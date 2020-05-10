import igraph
import numpy as np
from utils import utils as u
from utils import metrics as gm



print('====== Profiling results =======')

u.start_time()
g = igraph.Graph.Read_Picklez(fname= "./files/twitter_1K_picklez")
u.print_delta("load graph")
print('graph is directed ? : ',g.is_directed())
u.start_time()
gm.summary(g)
u.print_delta("get summary graph")

u.start_time()
gm.report(g)

u.print_delta("get report graph")

#gm.degree_distribution_plot(g,'dg_distri',loglog=False)

#gm.plot_degree_distribution(g)
#dD = g.degree_distribution(bin_width=10)
#print(dD)


#print(g.degree_distribution().bins())

# composante géante
print("==============GIANT ===============")
cl = g.components()
cl = g.as_undirected().components()
cl_sizes = cl.sizes()
#print ( 'sizes', len(cl_sizes) )
giant_component_index = cl_sizes.index(max(cl_sizes))
geant = cl.giant()
g.vs["component_id"] = cl.membership
# for i  in cl_sizes:
#       sub_g= g.vs[component_id_eq=i]
#       sub_degree = sub_g.vs.degree()  # vs.degree (mode=igraph.IN)
#       sub_max_deg = max(sub_degree)
#       print('found max degree : ', sub_max_deg, '  for sub ')
#       df_sub_degree = [sub_g.vs[idx] for idx, eb in enumerate(sub_degree) if eb == sub_max_deg]
#       g.vs[df_sub_degree[0]["name"]]["is_max_component"] = 1
#geant = gm.in_giant(g)
u.start_time()
gm.summary(geant)
u.print_delta("get giant component")
#geant=  g
print(" GIANT components :", geant.vcount())
gm.global_metrics(geant)

gm.get_max_vertex(g,igraph.ALL)
gm.get_max_vertex(g,igraph.IN)
gm.get_max_vertex(g,igraph.OUT)


gm.viz_graph(g,igraph.ALL,"graph_complete.pdf","drl",6)
gm.viz_graph(geant,igraph.ALL,"graph_giant.pdf","kk",6)

cfg = g.clus
cluster_fast_greedy(as.undirected(net))
plot(cfg, as.undirected(net))

print(" =========  End of Program ===")