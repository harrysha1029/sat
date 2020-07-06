from src.cnf import CNF, maximally_sensitive
from src.const import Assignment, PartialAssignment, TotalAssignment


def find_maximally_sensitive_partial_assignment(phi: CNF, m: int):
    n = phi.n_vars
