import itertools
import random

from src.normal_form import CNF
from src.assignment import completions
from src.const import Assignment, PartialAssignment, Permutation, TotalAssignment


def random_permutation(n: int) -> Permutation:
    sig = list(range(n))
    random.shuffle(sig)
    return sig


def ppz_encode(phi: CNF, x: TotalAssignment, sig: Permutation) -> TotalAssignment:
    pass


def ppz_decode(encoding: TotalAssignment, sig: Permutation) -> TotalAssignment:
    pass


def ppz_parallel_encode(
    phi: CNF, x: Assignment, sig: Permutation
):
    # enumerate all versions of phi with free coordinates of x filled in
    free_coords = [i for i, val in enumerate(x) if value == None]

    phis = [phi.copy() for _ in range(2**num_free(x))]
    completions = completions(x, num_free)

    enc = ""
    for var in sig:
        
        unit_clauses = [abs(v) for v in unit_c for unit_c in phi.clauses_with_width(1) for phi in phis]
        # extend encoding
        if var not in free_coords and var not in unit_clauses:
            enc += x[var]
        
        for i in range(len(phis)):
            phis[i].assign_single_variable(var, completions[i][var], in_place=True)

    return enc

def restrict(phi, restrictions):
    pass


def ppz_parallel_decode(phi: CNF, original_encoding, num_free_bits, sig: Permutation) -> Assignment:

    results = []
    # consider all possible locations of free coordinates
    all_possible_free_coords = itertools.combinations(range(1,n+1), num_free_bits)
    for free_coords in all_possible_free_coords:
        # enumerate phis and corresponding assignments
        phis = [phi.copy() for _ in range(2**num_free_bits)]
        
        partial_assigment = ['temp' if i not in free_coords else None for i in range(n)]
        completions = completions(partial_assigment, free_coords)
        completions = [x.replace('temp', None) for x in completions]
        
        # Completions have filled in free bits (all possible) and the stuff we have to fill in is None
        
        enc = original_encoding.copy()

        for var in sig:
            unit_clauses = [v for v in unit_c for unit_c in phi.clauses_with_width(1) for phi in phis]
            abs_unit_clauses = [abs(v) for v in unit_clauses]

            # var is in unit clause
            if var in abs_unit_clauses:
                v = 2*(var in unit_clauses) - 1
                next_vals = [v]*(2**num_free_bits)

            # var is free
            elif var in free_coords:
                next_vals = [x[var] for x in completions]

            # var is not free or unit
            else:
                next_vals = [int(enc[0])]*(2**num_free_bits)
                enc = enc[1:]

            # update phis
            for i in range(len(phis)):
                phis[i].assign_single_variable(var, next_vals[i])
                completions[i][var] = next_vals[i]
        
        x = agree_except_free(completions, free_coords)


        if all(evaluate(phi) for phi in phis) and x:
            results.append(x)

    return results

def agree_except_free(completions, free_coords):
    agreement = []

    for i in range(n):
        if i in free_coords:
            agreement += None
            continue
        
        for x in completions:
            if not(x[i] = completions[0][i]):
                return None
        
        agreement += completions[0][i]
    
    return agreement