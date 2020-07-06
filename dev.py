from typing import List, Union

from src.cnf import *
from src.draw import *
from src.random_sat import *
from src.sat_algs import *
from src.utils import *

phi = dist_R(6, 3, 5)
solns = all_solutions(phi)
draw_assignments(solns, phi)

ap = all_partial_assignments(5, 2)
print(ap)
for hi in ap:
    print(hi)

# draw_parity(5)

# assignment = ppz(phi, 1000)

# if assignment:
#     print_formula_with_assignment(phi, assignment)
#     print(sensitivity(phi, assignment))
#     print(avg_sensitivity(phi))
