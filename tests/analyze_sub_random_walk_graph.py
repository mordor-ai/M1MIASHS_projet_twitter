from igraph import *
from utils import utils as u
from utils import metrics as gm
from utils import plots
from utils import viz
from utils import random_walk as r
import matplotlib.pyplot as plt
import seaborn as sns

num_nodes: int = 100000
n_clusters = 3
folder_path = "../files/img/"
g: Graph = u.load_graph (num_nodes, True)
if (g):
    print ("loaded")
    # récupération des clusters
    g_undirected: Graph = g.as_undirected ( )
    cl = g_undirected.components ( )
    cl_sizes = cl.sizes ( )
    # g.clusters().giant()
    # print("nb of components : ", len(cl))
    # cl =g_undirected.clusters()
    # cl_sizes = cl.sizes()
    # print("nb of components : ",len(cl))

    # gm.get_top_n_for_page_rank(g, False, 10)
    print (" first 10 nodes ")
    gm.get_top_n_for_degree (g, ALL, 10)
    print (" first 10 IN nodes ")
    gm.get_top_n_for_degree (g, IN, 10)
    print (" first 10 OUT nodes ")
    gm.get_top_n_for_degree (g, OUT, 10)
    gm.summary (g)
    gm.global_metrics (g)
    gm.local_metrics (g)
    # gm.get_max_vertex(g, ALL)

    file_plot: str = 'histo_components_' + u.human_format (num_nodes)
    plots.plot_histo_components_distribution (cl, file_name=file_plot, folder=folder_path)
    # plt.bar(sorted(cl_sizes, reverse=True))
    file_plot: str = 'histo_degree_' + u.human_format (num_nodes)
    plots.plot_histo_degree_distribution (g, ALL, True, file_name=file_plot, folder=folder_path)
    file_plot: str = 'degree_' + u.human_format (num_nodes)
    plots.plot_plot_degree_distribution (g, file_name=file_plot, folder=folder_path)
    file_plot: str = 'scatter_frequency_degree_' + u.human_format (num_nodes)
    plots.plot_scatter_frequency_degree_distribution (g, ALL, file_name=file_plot, folder=folder_path)
    file_name: str = "graph_complet_" + u.human_format (num_nodes)
    # kk, lgl, drl
    viz.viz_graph (g, ALL, file_name, folder_path, "lgl", 0.1)
    file_name: str = "graph_complet_undirected" + u.human_format (num_nodes)
    viz.viz_graph (g_undirected, ALL, file_name, folder_path, "lgl", 0.1)

    print ("========== Random_walk==================")
    max_vertex = g.vs.select (_degree=g.maxdegree (mode=ALL))
    my_max_vertex_ind = max_vertex['name'][0]
    print ("node choosen for random walk : ", my_max_vertex_ind, "  ", max_vertex)
    random_walk_g: Graph = r.get_graph_random_walk (g, my_max_vertex_ind, 300)
    gm.summary (random_walk_g)
    gm.global_metrics (random_walk_g)
    gm.local_metrics (random_walk_g)
    file_plot: str = 'histo_degree_random_walk' + u.human_format (num_nodes)
    plots.plot_histo_degree_distribution (g=random_walk_g, modeInOutAll=ALL, isLog=True,
                                          file_name=file_plot, folder=folder_path)

    file_name: str = "graph_random_walk_" + u.human_format (num_nodes)
    # kk, lgl, drl
    viz.viz_graph (random_walk_g, ALL, file_name, folder_path, "fr", 1)
    file_name: str = "graph_random_walk_community_" + u.human_format (num_nodes)
    viz.viz_community (random_walk_g, ALL, file_name, folder_path, "", 1)
    file_name: str = 'graph_random_walk_hubs_' + u.human_format (num_nodes)
    viz.viz_hubs (random_walk_g, ALL, file_name, folder_path)
    file_name: str = 'graph_random_walk_authorities_' + u.human_format (num_nodes)
    viz.viz_authorities (random_walk_g, ALL, file_name, folder_path)

    gm.get_max_vertex (random_walk_g, ALL)
    gm.get_top_n_for_page_rank (random_walk_g, False, 10)
    gm.get_top_n_for_page_rank (random_walk_g, False, 10)


else:
    print ("error loading")
print ("=========================== END OF PROGRAM  ===============================")
