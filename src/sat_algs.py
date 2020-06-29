import itertools
from typing import Optional, List
import random

from src.utils import bitstrings

from src.cnf import (
    CNF,
    evaluate,
    Assignment,
    bitstrings,
    assign,
    simplify,
    assign_single_variable,
    evaluate_on_assignment,
    TotalAssignment,
    PartialAssignment,
)


def brute_force(phi: CNF) -> Optional[TotalAssignment]:
    for _sig in bitstrings(len(phi.variables)):
        sig = list(_sig)
        if evaluate_on_assignment(phi, sig):
            return sig
    return None


def all_solutions(phi: CNF) -> List[TotalAssignment]:
    sols = []
    for _sig in bitstrings(len(phi.variables)):
        sig = list(_sig)
        if evaluate_on_assignment(phi, sig):
            sols.append(sig)
    return sols


def ppz_once(phi: CNF) -> Optional[TotalAssignment]:
    n = phi.n_vars
    assignment : PartialAssignment = [None for _ in range(n)]
    for var in range(1, n + 1):
        if assignment[var - 1] is not None:  # Already been assigned
            continue

        val = None

        for clause in phi.clauses:
            if len(clause) == 1 and abs(clause[0]) == var:  # Forced
                val = clause[0] < 1
                break

        if val is None:  # Not forced
            val = random.choice([True, False])

        assignment[var - 1] = val
        phi = simplify(assign_single_variable(phi, var, val))
        if [] in phi.clauses:
            return None

    return [x for x in assignment if x is not None] # Type checking purposes, they should all be non none


def ppz(phi: CNF, iterations: int) -> Optional[TotalAssignment]:
    for _ in range(iterations):
        assignment = ppz_once(phi)
        if assignment:
            return assignment
    return None


if __name__ == "__main__":
    print(list(itertools.product([True, False], repeat=4)))
