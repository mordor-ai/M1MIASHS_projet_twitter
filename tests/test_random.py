from itertools import islice, takewhile
from igraph import *
from utils import random_walk as r
from utils import metrics as gm
from utils import viz

g: Graph = Graph.GRG (100, 0.2)
viz.viz_graph (g, ALL, "erdos", "./", label="id")
desired_length = 20
walk = list (islice (r.random_walk_iter (g, start=50), desired_length))
print (walk)
sub_g = g.induced_subgraph (walk)
gm.summary (sub_g)
gm.global_metrics (sub_g)
viz.viz_graph (sub_g, ALL, "sub_erdos", "./", label="id")
# finish = 15
# walk = list (takewhile (r.random_walk_iter (lambda x: x != finish, start=5))) + [finish]
