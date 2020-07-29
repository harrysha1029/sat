from src.normal_form import CNF
from src.assignment import mod, bitstrings

def mod_formula(n: int, mod: int) -> CNF:
    not_satisfying = [x for x in bitstrings(n) if (sum(x) % mod) == 0]
    phi = []
    for x in not_satisfying:
        clause = []
        for _i, v in enumerate(x):
            i = _i +1 
            clause.append(-i if v == 1 else i)
            phi.append(clause)
    return CNF(phi)

def block_mod_formula(n: int, k: int, mod: int) -> CNF:
    phi = []
    for i in range(n//k):
        d = {a: a + i*k for a in range(1, k+1)}
        phi.extend(mod_formula(k, mod).rename(d).clauses)
    return CNF(phi)

def mod_then_parity(n: int, k: int, mod: int) -> CNF:
    phi = []
    for i in range(n//k):
        if i == 0:
            phi.extend(mod_formula(k, mod).clauses)
        else:
            d = {a: a + i*k for a in range(1, k+1)}
            phi.extend(mod_formula(k, 2).rename(d).clauses)
    return CNF(phi)