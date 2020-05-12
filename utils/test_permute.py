from igraph import *
g: Graph=Graph.Erdos_Renyi(100, 0.2, directed=True)
layout = g.layout("kk")
plot(g, layout = layout)
g.permute_vertices()
layout = g.layout("kk")
plot(g, layout = layout)
g.transitivity_avglocal_undirected()