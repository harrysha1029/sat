import copy
from statistics import mean
from typing import List, Optional

from src.const import Assignment, Clause, PartialAssignment, TotalAssignment
from src.utils import all_partial_assignments, bitstrings

# Assignments is a list of truth assignments where the ith index contains the i+1s variables truth assignment


def lit_to_var(x):
    return abs(x)


class CNF:
    def __init__(self, clauses: Optional[List[Clause]] = None):
        if clauses is None:
            self.clauses = []
        else:
            self.clauses = clauses

    def __repr__(self):
        return "\n".join(
            map(
                lambda c: " ∨ ".join(
                    map(
                        lambda l: f"¬x{lit_to_var(l)}"
                        if l < 0
                        else f"x{lit_to_var(l)}",
                        c,
                    )
                ),
                self.clauses,
            )
        )

    def sorted(self):
        clauses = sorted([sorted(c) for c in self.clauses])
        return CNF(clauses)

    def __eq__(self, other):
        return self.sorted().clauses == other.sorted().clauses

    def __hash__(self):
        return hash(self.sorted().clauses.__repr__())

    @property
    def variables(self):
        return set(
            [lit_to_var(literal) for clause in self.clauses for literal in clause]
        )

    @property
    def n_vars(self):
        return max(self.variables)

    @property
    def literals(self):
        return set([literal for clause in self.clauses for literal in clause])


def print_assignment(x: Assignment) -> None:
    for i, a in enumerate(x):
        print(f"{i+1}:{a}", end=", ")
    print()


def print_formula_with_assignment(phi: CNF, x: Assignment) -> None:
    print(phi)
    print_assignment(x)
    print(assign_and_simplify(phi, x))


def flip_assignment_at(x: Assignment, var: int) -> Assignment:
    return [b if i != (var - 1) or b is None else True ^ b for i, b in enumerate(x)]


def sensitive_at(phi: CNF, x: TotalAssignment, var: int):
    val = evaluate_on_assignment(phi, x)
    return val != evaluate_on_assignment(phi, flip_assignment_at(x, var))


def sensitivity(phi: CNF, x: TotalAssignment) -> int:
    n = phi.n_vars
    assert len(x) == n
    val = evaluate_on_assignment(phi, x)
    return sum(
        val != evaluate_on_assignment(phi, flip_assignment_at(x, i))
        for i in range(1, n + 1)
    )


def avg_sensitivity(phi: CNF) -> float:
    return mean(sensitivity(phi, x) for x in bitstrings(phi.n_vars))


def assign(phi: CNF, assignment: Assignment) -> CNF:
    for var, val in enumerate(assignment):
        if val is None:
            continue
        assert isinstance(val, bool)
        phi = assign_single_variable(phi, var + 1, val)
    return phi


def assign_and_simplify(phi: CNF, assignment: Assignment) -> CNF:
    return simplify(assign(phi, assignment))


def assign_single_variable(phi: CNF, var: int, val: bool) -> CNF:
    new_clauses = []
    for c in phi.clauses:
        new_c = assign_clause_single_variable(c, var, val)
        new_clauses.append(new_c)
    return CNF(new_clauses)


def assign_clause_single_variable(clause: Clause, var: int, val: bool) -> Clause:
    new_clause: Clause = []
    for lit in clause:
        if lit_to_var(lit) == var:
            new_clause.append(val == (lit > 0))
            continue
        new_clause.append(lit)
    return new_clause


def simplify(phi: CNF) -> CNF:
    clauses = []
    for c in phi.clauses:
        if 1 in c:
            continue
        new_c = []
        for l in c:
            if l:
                new_c.append(l)
        clauses.append(new_c)
    return CNF(clauses)


def evaluate(phi: CNF) -> Optional[bool]:
    simplified = simplify(phi)
    if len(simplified.clauses) == 0:
        return True
    if [] in simplified.clauses:
        return False
    return None


def evaluate_on_assignment(phi: CNF, x: Assignment) -> Optional[bool]:
    return evaluate(assign(phi, x))


def impose_blanks(phi: CNF, blanks: List[int]) -> CNF:
    clauses = []
    for c in phi.clauses:
        new_c = []
        for l in c:
            if lit_to_var(l) not in blanks:
                new_c.append(l)
        clauses.append(new_c)
    return CNF(clauses)


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
    return [c for c in completions(x) if evaluate_on_assignment(phi, c)]


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
        if all(evaluate_on_assignment(phi, c) for c in completion):
            partial_sols.append(x)
    return partial_sols

def get_maximally_sensitive_assignments(phi, num_free):
    partial_assignments = all_partial_assignments(phi.n_vars, num_free)
    return [x for x in partial_assignments if maximally_sensitive(phi, x)]


def get_maximally_sensitive_solutions(phi, num_free):
    sols = get_all_partial_sols(phi, num_free)
    return [x for x in sols if maximally_sensitive(phi, x)]


if __name__ == "__main__":
    pass
