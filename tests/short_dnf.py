import itertools

from src.random_sat import sample
from src.sat_algs import all_solutions

# num variables, clause width, num clauses
n = 10, k = 3, m = 8

num_free_bits = 3
num_samples  = 10
true_blanks = [1,2,3]

# obtain k-CNFs
phis = sample(num_samples, dist_R, n, k, m)

for phi in phis:
  phi_blanks = impose_blanks(phi, true_blanks)
  
  # TODO: find maximally sensitive partial encoding x
  candidates = all_solutions(phi_blanks)

  # TODO: encode x with parallel_ppz

  # attempt to decode with all different blanks
  for blanks in list(itertools.combinations(range(1,n+1), 3)):
    psi = impose_blanks(phi, list(blanks))
    
    # TODO: attempt to decode psi
  
