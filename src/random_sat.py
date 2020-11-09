import random
from typing import Callable, Iterable, List
import math

from src.const import Assignment, Clause
from src.normal_form import CNF, all_cnfs, all_dnfs


def sample(
    num_sample, dist: Callable[[int, int, int], CNF], n: int, k: int
) -> Iterable[CNF]:
    for _ in range(num_sample):
        m = random.randrange(1, (n**k)*(2**k))
        while True:
            phi = dist(n, k, m)
            if phi.n_vars == n:
                yield phi
                break

def sample_m_range(
    num_sample, dist: Callable[[int, int, int], CNF], n: int, k: int, m_start, m_end
) -> Iterable[CNF]:
    for _ in range(num_sample):
        m = random.randrange(m_start, m_end)
        while True:
            phi = dist(n, k, m)
            if phi.n_vars == n:
                yield phi
                break

def sample_fix_num_clauses(
    num_sample, dist: Callable[[int, int, int], CNF], n: int, k: int, m: int
) -> Iterable[CNF]:
    for _ in range(num_sample):
        while True:
            phi = dist(n, k, m)
            if phi.n_vars == n:
                yield phi
                break



def sample_monotone_clause(n: int, k: int) -> Clause:
    multiplier = 1
    # multiplier = random.choice([1, -1])
    return [multiplier*random.randint(1, n) for _ in range(k)]

def sample_clause(n: int, k: int) -> Clause:
    # while True:
    #     clauses = [random.randint(1, n) * random.choice([1, -1]) for _ in range(k)]
    #     variables = [abs(l) for l in clauses]
    #     if (
    #         True not in [i and -i in clauses for i in range(n)]
    #         and len(set(variables)) > 1
    #     ):
    #         break
    clauses = [random.randint(1, n) * random.choice([1, -1]) for _ in range(k)]

    return clauses


def dist_R(n: int, k: int, m: int) -> CNF:
    clauses = [sample_clause(n, k) for _ in range(m)]
    return CNF(clauses)

def dist_monotone(n: int, k: int, m: int) -> CNF:
    clauses = [sample_monotone_clause(n, k) for _ in range(m)]
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
