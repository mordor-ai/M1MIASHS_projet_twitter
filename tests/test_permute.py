from igraph import *

g: Graph = Graph.Erdos_Renyi (100, 0.2, directed=True)
layout = g.layout ("kk")
plot (g, layout=layout, target="graph_permute_before.png")

layout = g.layout ("kk")
plot (g, layout=layout, target="graph_permute_after.png")
