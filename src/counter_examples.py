from pprint import pprint
from src.normal_form import CNF
from src.assignment import get_maximally_sensitive_solutions, get_free_coords
from src.draw import draw_solutions, draw_assignments_with_highlights, draw_assignments_with_mspas
from src.encode import ppz_parallel_encode
from src.sat_algs import all_solutions

def mspas_with_same_free_bits2():
    # NOTE: This counterexample was kind of hard to find
    phi = CNF([[1,-2], [1,-2,3], [1, 4], [2, -3, -4]])
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