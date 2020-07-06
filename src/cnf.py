from statistics import mean
from typing import List, Optional

from src.const import Assignment, Clause
from src.utils import bitstrings

# Assignments is a list of truth assignments where the ith index contains the i+1s variables truth assignment


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
                    map(lambda l: f"¬x{abs(l)}" if l < 0 else f"x{abs(l)}", c)
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
        return set([abs(literal) for clause in self.clauses for literal in clause])

    @property
    def n_vars(self):
        return max(self.variables)

    @property
    def literals(self):
        return set([literal for clause in self.clauses for literal in clause])


def flip_assignment_at(x: Assignment, ind: int) -> Assignment:
    return [b if i != (ind - 1) or b is None else True ^ b for i, b in enumerate(x)]


def print_assignment(x: Assignment) -> None:
    for i, a in enumerate(x):
        print(f"{i+1}:{a}", end=", ")
    print()


def print_formula_with_assignment(phi: CNF, x: Assignment) -> None:
    print(phi)
    print_assignment(x)
    print(assign_and_simplify(phi, x))


def sensitivity(phi: CNF, x: List[bool]) -> int:
    n = phi.n_vars
    assert len(x) == n  # Only works on total assignments
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
        if abs(lit) == var:
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
            if abs(l) not in blanks:
                new_c.append(l)
        clauses.append(new_c)
    return CNF(clauses)


if __name__ == "__main__":
    pass
