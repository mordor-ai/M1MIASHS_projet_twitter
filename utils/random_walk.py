# Random walk generator
# from  http://igraph.wikidot.com/python-recipes#toc6

from random import randint, choice
from igraph import *


def random_walk_iter(g: Graph, start=None):
    # The function below returns a generator that can be used to generate random walks from a given or a randomly selected starting point:
    current = randint (0, g.vcount ( ) - 1) if start is None else start
    while True:
        yield current
        # current = choice (g.successors (current))
        current = choice (g.neighbors (current))


def get_graph_random_walk(g: Graph, start=None, desired_length: int = 5):
    walk = list (islice (random_walk_iter (g, start=start), desired_length))
    return g.induced_subgraph (walk)
