from pprint import pprint
from src.normal_form import CNF
from src.assignment import *
from src.formulas import *
from src.draw import draw_solutions, draw_assignments_with_highlights, draw_assignments_with_mspas, draw_assignments
from src.encode import ppz_parallel_encode
from src.sat_algs import all_solutions, complement
from src.random_sat import *
from collections import Counter

def num_mspas_mod_3():
    for i in range(2, 10):
        phi = mod_formula(i, 3)
        mspas = get_maximally_sensitive_solutions(phi, 1)
        num_mspas = len(mspas)
        print(f"{i=}, {num_mspas=}")


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

def mspas_with_same_free_bits2():
    # NOTE: This counterexample was kind of hard to find
    # phi = CNF([[-1, 2, -3, 4], [1, -2, 4], [-1, -3, 5, -2], [3, 2, -4, -5]])

    # 4 sols
    phi = CNF([[-1, 2, -3, 4], [1, -2, 4, 3], [-1, -3, 5, -2, -4], [3, 2, -4, -5]])

    mspas = get_maximally_sensitive_solutions(phi, 2)
    print(phi)
    print("MSPAS")
    pprint(mspas)
    free_coords = [get_free_coords(x) for x in mspas]
    print(free_coords)
    relevant = [x for (x, i) in zip(mspas, free_coords) if i == (0, 4)]
    print()
    print("MSPAs with the same free bits:")
    print(relevant)
    print("Encodings:")
    for x in relevant:
        print(ppz_parallel_encode(phi, x, range(5)))

    draw_assignments_with_mspas(all_solutions(phi), relevant, phi, fname='mspas_with_same_free_bits.svg')
    draw_assignments(complement(all_solutions(phi)), phi, fname='falsifying.svg')

def mspas_with_same_free_bits():
    # NOTE: This counterexample was kind of hard to find
    phi = CNF([[-1, 2, -3], [1, -2, 4], [-1, -3, 5], [2, -4, -5]])
    mspas = get_maximally_sensitive_solutions(phi, 2)
    print(phi)
    print("MSPAS")
    pprint(mspas)
    free_coords = [get_free_coords(x) for x in mspas]
    relevant = [x for (x, i) in zip(mspas, free_coords) if i == (0, 4)]
    print()
    print("MSPAs with the same free bits:")
    print(relevant)
    print("Encodings:")
    for x in relevant:
        print(ppz_parallel_encode(phi, x, range(5)))

    draw_assignments_with_mspas(all_solutions(phi), relevant, phi, fname='mspas_with_same_free_bits.svg')


def counterexample_same_encoding_inconsistent():
    n = 5
    # phi = CNF([[-1, 4], [5], [-4, -2], [-1, 5]])
    phi = CNF([[5, 2], [-5, 3, 4], [-2, 5, 1], [2, 1]])
    mspas = get_maximally_sensitive_solutions(phi, 2)
    # mspa1 = [False, None, None, False, True] # Inconsistent b/c diverge in the 4th bit
    # mspa2 = [None, False, None, True, True]
    mspa1 = [True, True, None, None, False]
    mspa2 = [True, None, True, None, True]
    print(ppz_parallel_encode(phi, mspa1, list(range(n))))
    print(ppz_parallel_encode(phi, mspa2, list(range(n))))
    # extra = "\n MSPA1: 0**01, MSPA2: *0*11 both have encoding 0 but are inconsitent with one another"
    extra = "\n MSPA1: 11**0, MSPA2: 1*1*1 both have encoding 11 but are inconsistent with one another"

    draw_assignments(
        all_solutions(phi), phi, extra, fname="same_encoding_inconsistent.svg"
    )


# DATA 
"""
n   k   n/k mod  j           |S|    max_collisions
6   3   2   3    1*(n/k)     6^2    
9   3   3   3    1*(n/k)     6^3    12
8   4   2   4    2*(n/k)    12^2

"""