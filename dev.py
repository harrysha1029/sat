from typing import List, Union
from pprint import pprint

from collections import Counter

import itertools

import pandas as pd
from src.assignment import *
from src.draw import *
from src.encode import *
from src.random_sat import *
from src.sat_algs import *
from src.short_dnf import *
from src.utils import *
from src.examples import *
from src.formulas import *
from tqdm import tqdm

def num_mspas_mod_3():
    for i in range(2, 10):
        phi = mod_formula(i, 3)
        mspas = get_maximally_sensitive_solutions(phi, 1)
        num_mspas = len(mspas)
        print(f"{i=}, {num_mspas=}")

num_mspas_mod_3()


def search_for_something_worse_than_block_mod_three_for_n_over_k():
    # (4.877879681187904, 18318)
    n = 9
    k = 3
    phis = sample_m_range(100000, dist_R, n, k, 15, 30)
    running_average = (None, 0)
    for phi in phis:
        mspas = get_maximally_sensitive_solutions(phi, n/k)
        encs = [tuple(ppz_parallel_encode(phi, x, list(range(n)))) for x in mspas]
        c = Counter(encs)
        if len(encs) > 6**3:
            with open('YO.txt', 'a') as f:
                f.write("THIS ONE HAS MORE MSPAS THAN MOD3\n")
                f.write(str(phi))
        if len(c) > 0 and max(c.values()) > 12:
            with open('YO.txt', 'a') as f:
                f.write("THIS ONE HAS MORE COLLISIONS THAN MOD3\n")
                f.write(str(phi))
        num_mspas = len(mspas)
        if running_average[0] is None:
            running_average = (num_mspas, 1)
        else: 
            new_avg = (running_average[1]*running_average[0] + num_mspas)/(running_average[1] + 1)
            running_average = (new_avg, running_average[1] + 1)
        print(num_mspas)
        print(running_average)
        print(c)

# search_for_something_worse_than_block_mod_three_for_n_over_k()

def number_of_mspas_and_collisions_for_block_mod_3():
    n = 9
    k = 3
    mod = 3
    phi = block_mod_formula(n, k, mod)
    draw_solutions(phi)
    mspas = get_maximally_sensitive_solutions(phi, n/k)
    encs = [tuple(ppz_parallel_encode(phi, x, range(n))) for x in mspas]
    print(len(encs))
    print(Counter(encs))

# DATA 
"""
n   k   n/k mod  j           |S|    max_collisions
6   3   2   3    1*(n/k)     6^2    
9   3   3   3    1*(n/k)     6^3    12
8   4   2   4    2*(n/k)    12^2

"""