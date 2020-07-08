import random
from typing import Callable, List

from src.normal_form import CNF, all_cnfs, all_dnfs
from src.const import Assignment, Clause


def sample(
    num_sample, dist: Callable[[int, int, int], CNF], n: int, k: int, m: int
) -> List[CNF]:
    return [dist(n, k, m) for _ in range(num_sample)]


def sample_clause(n: int, k: int) -> Clause:
    return [random.randint(1, n) * random.choice([1, -1]) for _ in range(k)]


def dist_R(n: int, k: int, m: int) -> CNF:
    clauses = [sample_clause(n, k) for _ in range(m)]
    return CNF(clauses)


def dist_R_plus(n: int, k: int, m: int) -> CNF:
    # TODO
    pass


def dist_P(n: int, k: int, m: int) -> CNF:
    # TODO
    pass


def dist_P_sigma(n: int, k: int, m: int, sigma: Assignment) -> CNF:
    # TODO
    pass
