import copy
import itertools
from statistics import mean
from typing import List, Optional

from src.const import Assignment, Clause, PartialAssignment, TotalAssignment
from src.normal_form import CNF
from src.utils import all_partial_assignments, bitstrings

# Assignments is a list of truth assignments where the ith index contains the i+1s variables truth assignment


def print_assignment(x: Assignment) -> None:
    for i, a in enumerate(x):
        print(f"{i+1}:{a}", end=", ")
    print()


def print_formula_with_assignment(phi: CNF, x: Assignment) -> None:
    print(phi)
    print_assignment(x)
    print(phi.assign_and_simplify, x)


def flip_assignment_at(x: Assignment, var: int) -> Assignment:
    return [b if i != (var - 1) or b is None else True ^ b for i, b in enumerate(x)]


def sensitive_at(phi: CNF, x: TotalAssignment, var: int):
    val = phi.evaluate_on_assignment(x)
    return val != phi.evaluate_on_assignment(flip_assignment_at(x, var))


def sensitivity(phi: CNF, x: TotalAssignment) -> int:
    n = phi.n_vars
    assert len(x) == n
    val = phi.evaluate_on_assignment(x)
    return sum(
        val != phi.evaluate_on_assignment(flip_assignment_at(x, i))
        for i in range(1, n + 1)
    )


def avg_sensitivity(phi: CNF) -> float:
    return mean(sensitivity(phi, x) for x in bitstrings(phi.n_vars))


def is_total_assignment(x: Assignment) -> bool:
    return not (None in x)


def num_free(x: Assignment) -> int:
    return x.count(None)  # type: ignore


def assign_first_free(x: PartialAssignment, val: bool) -> Assignment:
    ind = x.index(None)
    new_assignment = copy.copy(x)
    new_assignment[ind] = val
    return new_assignment


def completions(x: Assignment, m: int = 0) -> List[TotalAssignment]:
    if num_free(x) == m:
        return [x]  # type: ignore
    assign1 = assign_first_free(x, True)  # type: ignore
    assign0 = assign_first_free(x, False)  # type: ignore

    return completions(assign0) + completions(assign1)


def satisfying_completions(phi: CNF, x: PartialAssignment) -> List[TotalAssignment]:
    return [c for c in completions(x) if phi.evaluate_on_assignment(c)]


def maximally_sensitive(phi: CNF, x: Assignment) -> bool:
    completion = completions(x)
    for _var, bit in enumerate(x):
        if bit is not None:
            if not any(sensitive_at(phi, sig, _var + 1) for sig in completion):
                return False
    return True


def get_all_partial_sols(phi, num_free):
    partial_assignments = all_partial_assignments(phi.n_vars, num_free)
    partial_sols = []
    for x in partial_assignments:
        completion = completions(x)
        if all(phi.evaluate_on_assignment(c) for c in completion):
            partial_sols.append(x)
    return partial_sols


def get_maximally_sensitive_solutions(phi, num_free):
    sols = get_all_partial_sols(phi, num_free)
    return [x for x in sols if maximally_sensitive(phi, x)]


def consistent(x: Assignment, y: Assignment):
    assert len(x) == len(y)
    for a, b in zip(x, y):
        if a is not None and b is not None and a != b:
            return False
    return True


def pairwize_consistent(l):
    for x, y in itertools.combinations(l, 2):
        if not consistent(x, y):
            return False
    return True

def get_free_coords(x):
    free = tuple(sorted([i for i, x in enumerate(x) if x is None]))
    return free



if __name__ == "__main__":
    pass
