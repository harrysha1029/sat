import copy
import itertools
from statistics import mean
from typing import List, Optional

from src.const import Assignment, Clause, PartialAssignment, TotalAssignment
from src.utils import all_partial_assignments, bitstrings, lit_to_var

# Assignments is a list of truth assignments where the ith index contains the i+1s variables truth assignment

class NormalForm:
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

    def rename_perm(self, pi, inplace=False):
        d = {i+1:j+1 for i, j in enumerate(pi)}
        return self.rename(d, inplace)

    def rename(self, d, in_place=False):
        def rename_literal(lit):
            var = abs(lit)
            sign = -1 if lit < 1 else 1
            if var in d:
                return sign*d[var]
            return lit

        new_clauses = [ ]
        for c in self.clauses:
            new_clauses.append([rename_literal(l) for l in c])
        if in_place:
            self.clauses = new_clauses 
            return self
        else: 
            return CNF(new_clauses)


    def sorted(self):
        clauses = sorted([sorted(c) for c in self.clauses])
        return self.__class__(clauses)

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

    def assign_on_variables(self, assignment: Assignment, vars: List[int]):
        for _var, val in enumerate(assignment):
            var = _var + 1
            if val is None:
                continue
            # assert isinstance(val, bool)
            if var in vars:
                self = self.assign_single_variable(var, val)
        return self

    def assign(self, assignment: Assignment):
        for var, val in enumerate(assignment):
            if val is None:
                continue
            assert isinstance(val, bool)
            self = self.assign_single_variable(var + 1, val)
        return self

    def permute(self, _sig, in_place=False):
        mapping = {i + 1: s + 1 for i, s in enumerate(_sig)}
        new_clauses = []
        for c in self.clauses:
            clause = []
            for l in c:
                sign = -1 if sign < 0 else 1
                new_var = mapping[abs(l)]
                clause.append(sign * new_var)
            new_clauses.append(clause)
        if in_place:
            self.clauses = new_clauses
            return
        else:
            return self.__class__(new_clauses)

    def assign_single_variable(self, var: int, val: bool, in_place=False):
        def assign_clause_single_variable(clause, var, val):
            new_clause: Clause = []
            for lit in clause:
                if lit_to_var(lit) == var:
                    new_clause.append(val == (lit > 0))
                    continue
                new_clause.append(lit)
            return new_clause

        new_clauses = []
        for c in self.clauses:
            new_c = assign_clause_single_variable(c, var, val)
            new_clauses.append(new_c)
        if in_place:
            self.clauses = new_clauses
            return self
        else:
            return self.__class__(new_clauses)

    def simplify(self, in_place=False):
        raise NotImplementedError

    def simplify_inplace(self):
        return self.simplify(True)

    def evaluate(self) -> Optional[bool]:
        raise NotImplementedError

    def assign_and_simplify(self, assignment: Assignment):
        return self.assign(assignment).simplify()

    def evaluate_on_assignment(self, assignment: Assignment) -> bool:
        return self.assign(assignment).evaluate()

    def clauses_with_width(self, j):
        return [c for c in self.clauses if len(c) == j]


def true_actually_in(l):
    return any(el == True and isinstance(el, bool) for el in l)


class CNF(NormalForm):
    def __repr__(self):
        return "CNF:\n" + "\n".join(
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

    def simplify(self, in_place=False):
        clauses = []
        for c in self.clauses:
            if true_actually_in(c):
                continue
            new_c = []
            for l in c:
                if l != False and l not in new_c:
                    new_c.append(l)
                if -l in new_c:
                    continue
            clauses.append(new_c)
        if in_place:
            self.clauses = clauses
            return self
        else:
            return CNF(clauses)

    def evaluate(self) -> Optional[bool]:
        simplified = self.simplify()
        if len(simplified.clauses) == 0:
            return True
        if [] in simplified.clauses:
            return False
        return None


class DNF(NormalForm):
    def __repr__(self):
        return "CNF:\n" + "\n".join(
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

    def simplify(self, in_place=False):
        clauses = []
        for c in self.clauses:
            if False in c:
                continue
            new_c = []
            for l in c:
                if l != True:
                    new_c.append(l)
            clauses.append(new_c)
        return CNF(clauses)

    def evaluate(self) -> Optional[bool]:
        simplified = self.simplify()
        if len(simplified.clauses) == 0:
            return False
        if [] in simplified.clauses:
            return True
        return None


def all_clauses(n, k):
    mon_clauses = itertools.combinations(range(1, n + 1), k)
    negations = list(itertools.product([1, -1], repeat=k))
    for c in mon_clauses:
        for n in negations:
            yield [x * i for x, i in zip(c, n)]


def all_cnfs(n, k, m):
    for clauses in itertools.combinations(all_clauses(n, k), m):
        yield CNF(clauses)


def all_dnfs(n, k, m):
    for clauses in itertools.combinations(all_clauses(n, k), m):
        yield DNF(clauses)