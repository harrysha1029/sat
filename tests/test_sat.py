from src.cnf import *
from src.sat_algs import *


def test_bf_unsat():
    phi = CNF([[-1, -2], [1, 2], [-1, 2], [1, -2]])
    sig = brute_force(phi)
    assert sig is None


def test_bf_sat():
    phi = CNF([[-1, -2, 3], [-2, 3]])
    sig = brute_force(phi)
    assert evaluate_on_assignment(phi, sig)


def test_assign_clause_single_variable_true():
    c = [1, 2, 3]
    var = 1
    val = True
    assert assign_clause_single_variable(c, var, val) == [True, 2, 3]


def test_assign_clause_single_variable_false():
    c = [1, 2, 3]
    var = 2
    val = False
    assert assign_clause_single_variable(c, var, val) == [1, False, 3]


def test_assign_single_variable_false():
    phi = CNF([[1, 2, 3], [-1, -2, 3]])
    phi2 = assign_single_variable(phi, 2, True)
    assert phi2.clauses == [[1, True, 3], [-1, False, 3]]


def test_evaluate_on_assignment_true():
    phi = CNF([[1, 2, 3], [-1, -2, 3]])
    assignment = [False, True, False]
    assert evaluate_on_assignment(phi, assignment)


def test_evaluate_on_assignment_false():
    phi = CNF([[1, 2, 3], [-1, -2, 3]])
    assignment = [True, True, False]
    assert not evaluate_on_assignment(phi, assignment)


def test_sensitivity():
    phi = CNF([[1, 2, 3], [-1, -2, 3]])
    assignment = [False, False, True]
    assert sensitivity(phi, assignment) == 1
