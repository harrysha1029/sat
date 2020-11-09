from src.sat_algs import all_solutions
from src.assignment import flip_assignment_at
import itertools

def is_monotonic(phi):
    sols = all_solutions(phi)
    for x in sols:
        plus_ones = [flip_assignment_at(x, i+1) for i in range(len(x)) if x[i] == 0]
        # print()
        # print()
        # print(x)
        # print()
        for f in plus_ones:
            # print(f)
            if f not in sols:
                return False
    return True