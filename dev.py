from src.cnf import *
from src.sat_algs import *
from src.utils import list_of_bool_to_binary_string
from src.draw import *
from typing import List, Union

phi = dist_R(5, 3, 10)
solns = all_solutions(phi)
draw_assignments(solns, phi)
# assignment = ppz(phi, 1000)

# if assignment:
#     print_formula_with_assignment(phi, assignment)
#     print(sensitivity(phi, assignment))
#     print(avg_sensitivity(phi))
