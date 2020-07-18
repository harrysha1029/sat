import itertools
import random
from copy import deepcopy
from typing import List
from collections import defaultdict

from src.assignment import completions, maximally_sensitive, get_maximally_sensitive_solutions, pairwize_consistent
from src.const import Assignment, PartialAssignment, Permutation, TotalAssignment
from src.normal_form import CNF
from src.utils import get_logger
from src.random_sat import sample_fix_num_clauses, dist_R
from src.sat_algs import all_solutions
from src.draw import draw_assignments


logger = get_logger(__name__)


def random_permutation(n: int) -> Permutation:
    sig = list(range(n))
    random.shuffle(sig)
    return sig


def ppz_encode(phi: CNF, x: TotalAssignment, sig: Permutation) -> TotalAssignment:
    pass


def ppz_decode(encoding: TotalAssignment, sig: Permutation) -> TotalAssignment:
    pass


def flatten(l):
    return list(itertools.chain(*l))


def get_literals_in_unit_clauses_from_lists_of_formulas(phis):
    return set(flatten(flatten([phi.clauses_with_width(1) for phi in phis])))


def ppz_parallel_encode(phi: CNF, x: Assignment, sig: Permutation) -> List[bool]:
    # enumerate all versions of phi with free coordinates of x filled in
    phi = phi.simplify()
    logger.info(f"ENCODING {x} with CNF {phi}")
    logger.info(f"{phi.clauses}")

    free_coords = [i + 1 for i, val in enumerate(x) if val == None]
    num_free = len(free_coords)
    phis = [deepcopy(phi) for _ in range(2 ** num_free)]
    _completions = completions(x)
    enc = []
    for _var in sig:
        var = _var + 1
        logger.info(f"{var}")
        unit_clauses = get_literals_in_unit_clauses_from_lists_of_formulas(phis)
        logger.info(f"unit_clauses: {unit_clauses}")

        if var in unit_clauses:
            logger.info(f"variable {var} is in a unit clauses, assigning True")
            for i in range(len(phis)):
                phis[i].assign_single_variable(
                    var, True, in_place=True
                ).simplify_inplace()
        elif -var in unit_clauses:
            logger.info(f"variable {var} is in a unit clauses, assigning False")
            for i in range(len(phis)):
                phis[i].assign_single_variable(
                    var, False, in_place=True
                ).simplify_inplace()
        else:
            logger.info(f"variable does not appear in unit clause, assigning..")
            for i in range(len(phis)):
                logger.info(f"formula {phis[i]}")
                logger.info(f"assigning {var}: {_completions[i][var-1]}")
                phis[i].assign_single_variable(
                    var, _completions[i][var - 1], in_place=True
                ).simplify_inplace()
                logger.info(f"updated formula: {phis[i]}")
            if var not in free_coords:
                logger.info(f"variable not free so appending to enc")
                enc.append(x[var - 1])
                logger.info(f"enc: {enc}")
    return enc  # type: ignore


def ppz_decode_guessed_free_bit_locations(phi, enc, free_coords, sig):
    num_free = len(free_coords)
    n = phi.n_vars
    phis = [deepcopy(phi) for _ in range(2 ** num_free)]

    partial_assigment = ["temp" if i + 1 not in free_coords else None for i in range(n)]
    _completions = completions(partial_assigment, free_coords)

    # Completions have filled in free bits (all possible) and the stuff we have to fill in is None

    enc = deepcopy(enc)

    for _var in sig:
        var = _var + 1
        unit_clauses = get_literals_in_unit_clauses_from_lists_of_formulas(phis)
        abs_unit_clauses = [abs(v) for v in unit_clauses]

        # var is free
        if var in free_coords:
            next_vals = [x[var - 1] for x in _completions]

        # var is in unit clause
        elif var in abs_unit_clauses:
            v = var in unit_clauses
            next_vals = [v] * (2 ** num_free)

        # var is not free or unit
        else:
            if (
                len(enc) == 0
            ):  # This one can't possibly be right b/c we ran out of input!
                return None
            next_vals = [enc[0]] * (2 ** num_free)
            enc = enc[1:]

        # update phis
        for i in range(len(phis)):
            phis[i].assign_single_variable(
                var, next_vals[i], in_place=True
            ).simplify_inplace()
            _completions[i][var - 1] = next_vals[i]

        # exit()

    decoding = agree_except_free(_completions, free_coords)

    if (
        all(_phi.evaluate() for _phi in phis)
        and decoding
        and len(enc) == 0
        and maximally_sensitive(phi, decoding)
    ):
        return decoding


def ppz_parallel_decode(
    phi: CNF, original_encoding, num_free_bits, sig: Permutation
) -> Assignment:
    phi = phi.simplify()
    results = []
    # consider all possible locations of free coordinates
    n = phi.n_vars
    all_possible_free_coords = itertools.combinations(range(1, n + 1), num_free_bits)

    for free_coords in all_possible_free_coords:
        decoding = ppz_decode_guessed_free_bit_locations(
            phi, original_encoding, free_coords, sig
        )
        if decoding:
            results.append(decoding)

    return results


def agree_except_free(_completions, free_coords):
    agreement = []
    n = len(_completions[0])

    for i in range(n):
        if i + 1 in free_coords:
            agreement.append(None)
            continue

        for x in _completions:
            if not (x[i] == _completions[0][i]):
                return None

        agreement.append(_completions[0][i])

    return agreement

def find_collision(n, k, m, j, num_sample=100):
    phis = sample_fix_num_clauses(num_sample, dist_R, n, k, m)
    for phi in phis:
        phi = phi.simplify_inplace()
        print(phi.clauses)
        sols = all_solutions(phi)
        mspas = get_maximally_sensitive_solutions(phi, j)
        enc2assign = defaultdict(list)
        for mspa in mspas:
            print(mspa)
            enc = ppz_parallel_encode(phi, mspa, list(range(n)))
            enc2assign[str(enc)].append(mspa)
        for k, v in enc2assign.items():
            if len(v) > 1:
                draw_assignments(sols, phi)
                print("Found a collision!!")
                print(k, v)
                if not pairwize_consistent(v):
                    print("Found a collision between inconsistent assignments!!")
                    print(k, v)
                    exit()

def counterexample_same_encoding_inconsistent():
    n = 5
    # phi = CNF([[-1, 4], [5], [-4, -2], [-1, 5]])
    phi = CNF([[5, 2], [-5, 3, 4], [-2, 5, 1], [2, 1]])
    mspas = get_maximally_sensitive_solutions(phi, 2)
    # mspa1 = [False, None, None, False, True] # Inconsistent b/c diverge in the 4th bit
    # mspa2 = [None, False, None, True, True]
    mspa1 = [True, True, None, None, False]
    mspa2 = [True, None, True, None, True]
    print(ppz_parallel_encode(phi, mspa1, list(range(n))))
    print(ppz_parallel_encode(phi, mspa2, list(range(n))))
    # extra = "\n MSPA1: 0**01, MSPA2: *0*11 both have encoding 0 but are inconsitent with one another"
    extra = "\n MSPA1: 11**0, MSPA2: 1*1*1 both have encoding 11 but are inconsistent with one another"

    draw_assignments(all_solutions(phi), phi, extra)