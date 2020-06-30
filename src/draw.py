import itertools

import networkx as nx

from src.utils import bitstrings, list_of_bool_to_binary_string, xor


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


def draw_assignments(assignments, phi=None):
    G = nx.DiGraph(label=str(phi))
    for x, y in itertools.combinations(assignments, 2):
        if sum(x) > sum(y):
            x, y = y, x
        diff = xor(x, y)
        if sum(diff) == 1:
            G.add_edge(
                list_of_bool_to_binary_string(x),
                list_of_bool_to_binary_string(y),
                label=str(diff.index(1) + 1),
            )
    draw_graph(G)


def draw_2n(n):
    strings = bitstrings(n)
    draw_assignments(strings)
