from igraph import *
from utils import utils as u
from utils import metrics as gm
from utils import plots
from utils import viz
from utils import networkcentrality as nc
from utils import random_walk as r
import matplotlib.pyplot as plt
import seaborn as sns

num_nodes: int = 1000
n_clusters = 2
folder_path = "./files/img/"
g: Graph = u.load_graph (num_nodes, True)

if g:

    print ("loaded")
    #     g.vs["twitter_name"]=""
    ## nettoyage des neouds non connectés
    # https://stackoverflow.com/questions/29332220/python-igraph-delete-vertices-from-a-graph
    to_delete = g.vs.select (_degree=0)
    if to_delete:
        to_delete_ids = [v.index for v in to_delete]
        g.delete_vertices (to_delete_ids)
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
    gm.print_first_top (g)
    gm.global_metrics (g)

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

    file_name: str = "graph_complet_degree_all_" + u.human_format (num_nodes)
    # kk, lgl, drl
    degree = g.degree (mode=ALL)
    viz.viz_graph (g, degree, file_name, folder_path, "fr", 0.1)

    file_name: str = "graph_complet_closeness_all_" + u.human_format (num_nodes)
    # kk, lgl, drl
    degree = g.closeness (mode=ALL)
    viz.viz_graph (g, degree, file_name, folder_path, "fr", 0.1)

    file_name: str = "graph_complet_page_rank_" + u.human_format (num_nodes)
    # kk, lgl, drl
    degree = g.pagerank (directed=True)
    viz.viz_graph (g, degree, file_name, folder_path, "fr", 0.1)
    file_name: str = "graph_complet_betweeness_" + u.human_format (num_nodes)
    # kk, lgl, drl
    degree = g.betweenness (directed=True)
    viz.viz_graph (g, degree, file_name, folder_path, "fr", 0.1)

    # g_undirected.component_di
    # boucle sur les clusters
    index: int = 0

    # on affiche que les    n_clusters  plus gros clusters
    for cluster in sorted (cl, key=len, reverse=True)[0:n_clusters - 1]:
        index += 1
        print ("=================component N° : ", str (index), "=====================")
        # print ("list : ".join(str(idx) for idx in cluster))
        current_sub_graph: Graph = g.induced_subgraph (cluster, implementation="auto")
        to_delete = current_sub_graph.vs.select (_degree=0)
        if to_delete:
            to_delete_ids = [v.index for v in to_delete]
            current_sub_graph.delete_vertices (to_delete_ids)
        u.save_graph (current_sub_graph, 'twitter_' + u.human_format (num_nodes) + '_cluster_' + str (index),
                      './files/pickle/', True)
        gm.global_metrics (current_sub_graph)
        gm.local_metrics (current_sub_graph)
        file_plot: str = 'histo_degree_' + u.human_format (num_nodes) + '_' + str (index)
        plots.plot_histo_degree_distribution (g=current_sub_graph, modeInOutAll=ALL, isLog=True,
                                              file_name=file_plot, folder=folder_path)

        file_name: str = "graph_" + str (index) + "_degree_all_" + u.human_format (num_nodes)
        # kk, lgl, drl
        degree = current_sub_graph.degree (mode=ALL)
        viz.viz_graph (current_sub_graph, degree, file_name, folder_path, "fr", 0.1)

        file_name: str = "graph_" + str (index) + "_closeness_all_" + u.human_format (num_nodes)
        # kk, lgl, drl
        degree = current_sub_graph.closeness (mode=ALL)
        viz.viz_graph (current_sub_graph, degree, file_name, folder_path, "fr", 0.1)

        file_name: str = "graph_" + str (index) + "_page_rank_" + u.human_format (num_nodes)
        # kk, lgl, drl
        degree = current_sub_graph.pagerank (directed=True)
        viz.viz_graph (current_sub_graph, degree, file_name, folder_path, "fr", 0.1)
        file_name: str = "graph_" + str (index) + "_betweeness_" + u.human_format (num_nodes)
        # kk, lgl, drl
        degree = current_sub_graph.betweenness (directed=True)
        viz.viz_graph (current_sub_graph, degree, file_name, folder_path, "fr", 0.1)

        file_name: str = "graph_community_" + str (index) + "_" + u.human_format (num_nodes)
        viz.viz_community (current_sub_graph, ALL, file_name, folder_path, "", 0.1)
        file_name: str = "graph_diameter_" + str (index) + "_" + u.human_format (num_nodes)
        viz.viz_diameter (current_sub_graph, file_name, folder_path)

        gm.print_first_top (current_sub_graph)
        # gm.get_max_vertex (current_sub_graph, ALL)
        # gm.get_top_n_for_page_rank (current_sub_graph, False, 10)
        # gm.get_top_n_for_page_rank (current_sub_graph, False, 10)
    print ("========== end of components ==================")

    print ("========== Rich Club ==================")
    rich_g: Graph = gm.richclub (g.as_undirected ( ), 0.2)
    to_delete = rich_g.vs.select (_degree=0)
    if to_delete:
        to_delete_ids = [v.index for v in to_delete]
        rich_g.delete_vertices (to_delete_ids)
    u.save_graph (rich_g, 'twitter_' + u.human_format (num_nodes) + '_rich_club',
                  './files/pickle/', True)

    gm.global_metrics (rich_g)
    gm.local_metrics (rich_g)
    file_name: str = "graph_rich_club" + str (index) + "_" + u.human_format (num_nodes)
    # kk, lgl, drl
    viz.viz_graph (rich_g, ALL, file_name, folder_path, "fr", 1)
    file_name: str = "graph_rich_club_community_" + u.human_format (num_nodes)
    viz.viz_community (rich_g, ALL, file_name, folder_path, "", 1)
    file_name: str = 'graph_rich_club_hubs_' + u.human_format (num_nodes)
    viz.viz_hubs (rich_g, ALL, file_name, folder_path)
    file_name: str = 'graph_rich_club_authorities_' + u.human_format (num_nodes)
    viz.viz_authorities (rich_g, ALL, file_name, folder_path)

    gm.print_first_top (current_sub_graph)
    # gm.get_max_vertex (rich_g, ALL)
    # gm.get_top_n_for_page_rank (rich_g, False, 10)
    # gm.get_top_n_for_degree (rich_g, False, 10)



else:
    print ("error loading")
print ("=========================== END OF PROGRAM  ===============================")
