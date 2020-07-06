import random

from src.cnf import CNF
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
    phi: CNF, x: TotalAssignment, sig: Permutation
) -> TotalAssignment:
    pass


def ppz_parallel_decode(encoding: TotalAssignment, sig: Permutation) -> TotalAssignment:
    pass
