import itertools
import math

from src.assignment import get_maximally_sensitive_solutions
from src.normal_form import CNF, all_cnfs
from src.draw import draw_assignments
from src.random_sat import dist_R, sample
from src.sat_algs import all_solutions
from tqdm import tqdm
import os
import ast

def num_nfs(n, k, m):
    return math.comb(math.comb(n, k)*2**k, m)

def read_index(fname, index):
    with open(fname, 'r') as f:
        for i, l in enumerate(f):
            print(i, l)
            if i == index:
                print(l)
                return l

def get_ith_cnf(index, n, k, m):
    fname = f'cnfs_list_n{n}_k{k}_m{m}.txt'
    if os.path.isfile(fname):
        string = read_index(fname, index)
        clauses = ast.literal_eval(string)
        return CNF(clauses)
    else:
        for i, phi in enumerate(all_cnfs(n, k, m)):
            if i == index:
                return phi

def cnfs_file(n, k, m):
    fname = f'cnfs_list_n{n}_k{k}_m{m}.txt'
    for phi in tqdm(all_cnfs(n, k, m), total=num_nfs(n,k,m)):
        with open(fname, 'a') as f:
            f.write(str(list(phi.clauses)))
            f.write('\n')

COLS = ['index', 'n', 'm', 'k', 'n_max_sens']
def generate_short_dnf_stats(n, k, m, nfree):
    fname = f'cnfs_n{n}_k{k}_m{m}_nfree{nfree}.csv'
    for i, phi in tqdm(enumerate(all_cnfs(n, k, m)), total=num_nfs(n,k,m)):
        with open(fname, 'a') as f:
            max_sens = get_maximally_sensitive_solutions(phi, nfree)
            num_max_sens = len(max_sens)
            f.write(", ".join(map(str, [i, n, k, m, num_max_sens])))
            f.write('\n')

def get_bound(n, k):
    return 2 ** (n-n/k)

def short_dnf():
    # num variables, clause width, num clauses
    n, k = 5, 3
    m = int(2 ** (n ** 0.5))
    bound = 2 ** (n - n / k)

    num_samples = 1000
    num_free_bits = 2
    num_fixed = n-num_free_bits

    assert 2 ** (num_fixed) * math.comb(n, num_fixed) > bound

    # obtain k-CNFs
    # phis = sample(num_samples, dist_R, n, k, m)
    # print(n)
    for i, phi in tqdm(all_cnfs(n, k, m)):
        # find maximally sensitive partial encoding x
        solns = all_solutions(phi)
        max_sens = get_maximally_sensitive_solutions(phi, num_free_bits)
        # draw_assignments(solns, phi)
        if len(max_sens) > bound +1:
            draw_assignments(solns, phi, fname=f'counter_examples/{example_counter}.svg')
            example_counter += 1
            print("=========================")
            print("CONJECTURE WRONG :O:O:O")
            print(phi)
            print(max_sens)
            num_max_sens = len(max_sens)
            print(f"{n=}\n {k=}\n {m=}\n {bound=}\n {num_free_bits=}\n {num_max_sens=}")

        # TODO: encode x with parallel_ppz

        # attempt to decode with all different locations of free bits
        # for free in list(itertools.combinations(range(1, n + 1), 3)):
        #   psi = impose_blanks(phi, list(free))

        # TODO: attempt to decode psi
