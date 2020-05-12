from  igraph import *
from utils import utils as u
from utils import metrics as gm
import matplotlib.pyplot as plt
import seaborn as sns
num_nodes: int = 1000000

g:Graph = u.load_graph(num_nodes,True)
if (g):
    print("loaded")
    # récupération des clusters
    g_undirected: Graph = g.as_undirected()
    cl = g_undirected.components()
    cl_sizes = cl.sizes()
    #print("nb of components : ", len(cl))
    #cl =g_undirected.clusters()
    #cl_sizes = cl.sizes()
   # print("nb of components : ",len(cl))

    gm.get_top_n_for_page_rank(g, False, 10)
    gm.get_top_n_for_degree(g, ALL, 10)
    gm.summary(g)
    #gm.get_max_vertex(g, ALL)

    file_plot: str = 'histo_components_' + u.human_format(num_nodes)
    gm.plot_components_distribution(cl,file_plot)
    #plt.bar(sorted(cl_sizes, reverse=True))
    file_plot: str = 'histo_degree_' + u.human_format(num_nodes)
    gm.plot_histo_degree_distribution(g,ALL,True,file_plot)
    file_plot: str = 'degree_' + u.human_format(num_nodes)
    gm.degree_distribution_plot(g,filename=file_plot)
    file_plot: str = 'histo_frequency_degree_' + u.human_format(num_nodes)
    gm.plot_frequency_degree_distribution(g,ALL,file_plot)

    #g_undirected.component_di
    # boucle sur les clusters
    index: int=0
    # on affiche que les 10 plus gros clusters
    for cluster  in sorted(cl,key=len,reverse=True)[0:10]:
        index+=1
        print("=================component N° : ",str(index),"=====================")
        #print ("list : ".join(str(idx) for idx in cluster))
        current_sub_graph:Graph = g.induced_subgraph(cluster,implementation="auto")
        gm.summary(current_sub_graph)
        file_plot :str = 'histo_degree_'+u.human_format(num_nodes)+'_'+str(index)
        gm.plot_histo_degree_distribution(g=current_sub_graph,modeInOutAll=ALL,isLog=True,file_name=file_plot)
        #gm.global_metrics(current_sub_graph)
        file_name: str = "graph_"+str(index)+"_"+u.human_format(num_nodes)
        gm.viz_graph(current_sub_graph, ALL, file_name, "drl", 6)
        gm.get_max_vertex(current_sub_graph,ALL)
        gm.get_top_n_for_page_rank(current_sub_graph,False,10)
        gm.get_top_n_for_page_rank(current_sub_graph,False,10)
else:
    print("error loading")
    print("=========================== END OF PROGRAM  ===============================")