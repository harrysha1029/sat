from typing import List, Union
from pprint import pprint

import pandas as pd
from src.assignment import *
from src.draw import *
from src.encode import *
from src.random_sat import *
from src.sat_algs import *
from src.short_dnf import *
from src.utils import *
from src.counter_examples import *

from tqdm import tqdm

mspas_with_same_free_bits2()

# n, k, j, m = 4, 3, 1, 10

# for _ in tqdm(range(100000)):
#     phi = dist_R(n, k, m)
#     mspas = get_maximally_sensitive_solutions(phi, j)
#     free_coords = [get_free_coords(x) for x in mspas]
#     if len(set(free_coords)) < len(free_coords):
#         print(phi.clauses)
#         print(free_coords)
#         # relevant = [x for (x, i) in zip(mspas, free_coords) if i == (0, 4)]
#         print("HI found counterexample")
#         exit()

# draw_assignments(block_mod(6, 3, 3))
# draw_assignments(complement(block_mod(4, 2, 2)))

# draw_as_subset(block_mod(6, 3, 3), 6)
# phi = CNF([[-1, 2, -3], [1, -2, 4], [-1, -3, 5], [2, -4, -5]])
# draw_falsifying(phi, fname="falsifying.svg")