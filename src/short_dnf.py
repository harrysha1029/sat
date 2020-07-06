import itertools

from src.cnf import get_maximally_sensitive_solutions, impose_blanks
from src.draw import draw_assignments
from src.random_sat import dist_R, sample
from src.sat_algs import all_solutions
from tqdm import tqdm

# def enumerate_dnfs()


def short_dnf():
    # num variables, clause width, num clauses
    n, k, = 5, 3
    m = int(2 ** (n ** 0.5))
    bound = 2 ** (n - n / k)

    num_samples = 100
    num_free_bits = 2

    assert 2 ** (n - num_free_bits) > bound
    return

    # obtain k-CNFs
    phis = sample(num_samples, dist_R, n, k, m)
    print(n)

    for phi in tqdm(phis):
        # find maximally sensitive partial encoding x
        solns = all_solutions(phi)
        draw_assignments(solns, phi)
        max_sens = get_maximally_sensitive_solutions(phi, num_free_bits)
        if len(max_sens) > bound +1:
            print("CONJECTURE WRONG :O:O:O")
            print(phi)
            print(max_sens)
            num_max_sens = len(max_sens)
            print(f"{n=}, {k=}, {m=}, {bound=}, {num_free_bits=}, {num_max_sens=}")
            return

        # TODO: encode x with parallel_ppz

        # attempt to decode with all different locations of free bits
        # for free in list(itertools.combinations(range(1, n + 1), 3)):
        #   psi = impose_blanks(phi, list(free))

        # TODO: attempt to decode psi
