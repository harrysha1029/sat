import itertools
import math
from typing import Iterable

import networkx as nx
from src.assignment import completions
from src.const import Assignment, TotalAssignment
from src.normal_form import NormalForm
from src.sat_algs import all_falsifying, all_solutions
from src.utils import bitstrings, list_of_bool_to_binary_string, xor, flatten


def draw_graph(graph: nx.Graph, fname: str = "diagram.svg", **kwargs):
    """Draws a graph and saves it to fname

    Args:
        graph (nx.Graph): graph to draw
        fname (str, optional): name of the file to save to.
                               Defaults to "test.svg".
    """
    agraph = nx.drawing.nx_agraph.to_agraph(graph)
    agraph.layout("dot")
    agraph.draw(fname, **kwargs)


def make_graph(assignments, phi=None, extra_text=""):
    G = nx.DiGraph(label=str(phi) + "\n" + extra_text)
    G.add_nodes_from([list_of_bool_to_binary_string(x) for x in assignments])
    for x, y in itertools.combinations(assignments, 2):
        if sum(x) > sum(y):
            x, y = y, x
        diff = xor(x, y)
        if sum(diff) == 1:
            G.add_edge(
                list_of_bool_to_binary_string(x),
                list_of_bool_to_binary_string(y),
                label=str(diff.index(True) + 1),
            )
    return G


def draw_assignments(
    assignments: Iterable[TotalAssignment], phi=None, extra_text="", **kwargs
):
    G = make_graph(assignments, phi, extra_text)
    draw_graph(G, **kwargs)


def draw_assignments_with_highlights(
    assignments: Iterable[TotalAssignment],
    highlights,
    phi=None,
    extra_text="",
    **kwargs
):
    G = make_graph(assignments, phi, extra_text)
    for x in highlights:
        G.nodes[list_of_bool_to_binary_string(x)]["style"] = "filled"
        G.nodes[list_of_bool_to_binary_string(x)]["fillcolor"] = "red"
    draw_graph(G, **kwargs)


def draw_assignments_with_mspas(
    assignments: Iterable[TotalAssignment], mspas, phi=None, extra_text="", **kwargs
):
    G = make_graph(assignments, phi, extra_text)
    cols = ["red", "green", "blue"]
    for x, col in zip(mspas, itertools.cycle(cols)):
        for comp in completions(x):
            G.nodes[list_of_bool_to_binary_string(comp)]["style"] = "filled"
            G.nodes[list_of_bool_to_binary_string(comp)]["fillcolor"] = col
    draw_graph(G, **kwargs)

def draw_both(phi, **kwargs):
    draw_solutions(phi, fname='sols.svg', **kwargs)
    draw_falsifying(phi, fname='falsifying.svg', **kwargs)


def draw_solutions(phi: NormalForm, **kwargs):
    sols = all_solutions(phi)
    draw_assignments(sols, phi, extra_text='Showing satisfying assignments', **kwargs)


def draw_falsifying(phi: NormalForm, **kwargs):
    sols = all_falsifying(phi)
    draw_assignments(sols, phi, extra_text="Showing falsifying assignments", **kwargs)


def draw_as_subset(
    assignments: Iterable[TotalAssignment], n: int, phi=None, extra_text="", **kwargs
):
    draw_assignments_with_highlights(
        bitstrings(n), assignments, phi, extra_text, **kwargs
    )


def draw_2n(n: int):
    strings = list(bitstrings(n))
    draw_assignments(strings)


def draw_parity(n: int):
    strings = [x for x in bitstrings(n) if (sum(x) % 2) == 1]
    draw_assignments(strings)


def draw_mod(n: int, mod):
    strings = [x for x in bitstrings(n) if (sum(x) % mod) != 0]
    draw_assignments(strings)


def draw_block_mod(n: int, k, mod):
    nk = n // k
    remainder = n % k
    assignments = itertools.product(
        [x for x in bitstrings(k) if sum(x) % mod != 0], repeat=nk
    )
    if remainder > 0:
        assignments = itertools.product(
            (assignments, [x for x in bitstrings(remainder) if sum(x) % mod != 0])
        )
    assignments = [flatten(x) for x in assignments]

    draw_assignments(assignments)
