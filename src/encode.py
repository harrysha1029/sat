import itertools
import random

from src.normal_form import CNF
from src.assignment import completions, maximally_sensitive
from src.const import Assignment, PartialAssignment, Permutation, TotalAssignment
from copy import deepcopy
from typing import List


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

def ppz_parallel_encode(
    phi: CNF, x: Assignment, sig: Permutation
) -> List[bool]:
    # enumerate all versions of phi with free coordinates of x filled in
    free_coords = [i+1 for i, val in enumerate(x) if val == None]
    num_free = len(free_coords)
    phis = [deepcopy(phi) for _ in range(2**num_free)]
    _completions = completions(x)
    enc = []
    for _var in sig:
        var = _var + 1
        unit_clauses = get_literals_in_unit_clauses_from_lists_of_formulas(phis)

        if var in unit_clauses:
            for i in range(len(phis)):
                phis[i].assign_single_variable(var, True, in_place=True).simplify_inplace()
        elif -var in unit_clauses:
            for i in range(len(phis)):
                phis[i].assign_single_variable(var, False, in_place=True).simplify_inplace()
        else:
            for i in range(len(phis)):
                phis[i].assign_single_variable(var, _completions[i][var-1], in_place=True).simplify_inplace()
            if var not in free_coords:
                enc.append(x[var-1]) 
    return enc # type: ignore

def ppz_decode_guessed_free_bit_locations(phi, enc, free_coords, sig):
    num_free = len(free_coords)
    n = phi.n_vars
    phis = [deepcopy(phi) for _ in range(2**num_free)]
    
    partial_assigment = ['temp' if i + 1 not in free_coords else None for i in range(n)]
    _completions = completions(partial_assigment, free_coords)
    
    # Completions have filled in free bits (all possible) and the stuff we have to fill in is None
    
    enc = deepcopy(enc)

    for _var in sig:
        var = _var + 1
        unit_clauses = get_literals_in_unit_clauses_from_lists_of_formulas(phis)
        abs_unit_clauses = [abs(v) for v in unit_clauses]

        # var is free
        if var in free_coords:
            next_vals = [x[var-1] for x in _completions]

        # var is in unit clause
        elif var in abs_unit_clauses:
            v = var in unit_clauses
            next_vals = [v]*(2**num_free)

        # var is not free or unit
        else:
            if len(enc) == 0: # This one can't possibly be right b/c we ran out of input!
                return None
            next_vals = [enc[0]]*(2**num_free) 
            enc = enc[1:]

        # update phis
        for i in range(len(phis)):
            phis[i].assign_single_variable(var, next_vals[i], in_place=True).simplify_inplace()
            _completions[i][var-1] = next_vals[i]

        # exit()
    
    decoding = agree_except_free(_completions, free_coords)

    if all(_phi.evaluate() for _phi in phis) and decoding and len(enc) == 0 and maximally_sensitive(phi, decoding):
        return decoding

def ppz_parallel_decode(phi: CNF, original_encoding, num_free_bits, sig: Permutation) -> Assignment:
    results = []
    # consider all possible locations of free coordinates
    n = phi.n_vars
    all_possible_free_coords = itertools.combinations(range(1,n+1), num_free_bits)


    for free_coords in all_possible_free_coords:
        decoding = ppz_decode_guessed_free_bit_locations(phi, original_encoding, free_coords, sig)
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
            if not(x[i] == _completions[0][i]):
                return None
        
        agreement.append(_completions[0][i])
    
    return agreement