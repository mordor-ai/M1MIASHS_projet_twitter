# -*- coding: utf-8 -*-

"""
igraphplus.metrics
~~~~~~~~~~~~~~~~~

This module contains the metrics for graphs.
"""
import matplotlib.pyplot as plt
import seaborn as sns
from igraph import *
import numpy as np
from utils import utils as u
from collections import Counter
from operator import itemgetter


def efficiency(g: Graph, initial=0, removed=0):
    """Efficiency calculation"""
    result = 0.0
    paths = g.shortest_paths ( )
    if g.is_directed ( ):
        for path in paths:
            for distance in path:
                if 0 < distance < float ('Inf'):
                    result += float (1) / distance
    else:
        for index, path in enumerate (paths):
            for distance in path[index + 1:]:
                if 0 < distance < float ('Inf'):
                    result += float (2) / distance

    n = g.vcount ( )
    if initial:
        n = initial
    if removed:
        n -= removed

    result /= n * (n - 1)
    return result


def degree_distribution(g: Graph):
    """ bin = [min_i, max_i, amount)"""
    distribution = {}
    for b in g.degree_distribution ( ).bins ( ):
        if b[2]:
            distribution[b[0]] = b[2]
    return distribution


def degree_properties(g: Graph):
    """ Response with min, max, average degree and it's std"""
    import numpy

    degrees = numpy.array (g.degree ( ))
    min_degree = degrees.min ( )
    max_degree = degrees.max ( )
    mean_degree = degrees.mean ( )
    std_degree = degrees.std ( )
    return min_degree, max_degree, mean_degree, std_degree


def summary(g: Graph):
    degree_stats = degree_properties (g)
    connected = 'connected' if (g.is_connected ( )) else 'unconnected'
    directed = 'directed' if (g.is_directed ( )) else 'undirected'
    deg = '(%d, %0.2f ± %0.2f, %d)' % (degree_stats[0], degree_stats[2], degree_stats[3], degree_stats[1])
    return 'N:%d E:%d %s %s Components:%d Degree:%s' % (
        g.vcount ( ), g.ecount ( ), connected, directed, len (g.components ( )), deg)


def report(g: Graph):
    degree_stats = degree_properties (g)
    print ('Graph is: %s, %s' %
           ('Connected' if (g.is_connected ( )) else 'Disconnected',
            'Directed' if (g.is_directed ( )) else 'Undirected'))
    print ('Number of nodes: %d' % g.vcount ( ))
    print ('Number of edges: %d' % g.ecount ( ))
    print ('Number of components: %d' % len (g.components ( )))
    print ('Degree: min = %d, max = %d, mean = %0.2f, std = %0.2f' % (
        degree_stats[0], degree_stats[1], degree_stats[2], degree_stats[3]))


# from  https://stackoverflow.com/questions/25147163/identity-of-nodes-in-the-giant-component-in-igraph-with-python
def in_giant(g: Graph):
    largest = g.clusters ( ).giant ( )
    return largest


def in_giant_alt(G: Graph):
    cl = G.components ( ).giant ( )
    cl_sizes = cl.sizes ( )
    giant_component_index = cl_sizes.index (max (cl_sizes))
    return [x == giant_component_index for x in cl.membership]


def global_metrics(g: Graph):
    u.start_time ( )
    summary (g)
    print ("GLOBAL MEASURES")
    print ("Connected:", g.is_connected ( ))
    print ("Density:", g.density ( ))
    print ("Diameter:", g.diameter ( ))
    print ("Clustering Coefficient:", g.transitivity_undirected ( ))
    print ("Average Local Clustering Coefficient:", g.transitivity_avglocal_undirected ( ))
    print ("Average Degree:", mean (g.degree ( )))
    print ("Max Degree:", g.maxdegree ( ))
    # print("Average Betweenness:", mean(g.betweenness()))
    # print("Max Betweenness:", max(g.betweenness()))
    # print("Average Closeness:", mean(g.closeness()))
    # print("Max Closeness:", max(g.closeness()))
    #  print("mean distance directed", g.v)
    u.print_delta ("get global metrics ")


def local_metrics(g: Graph):
    u.start_time ( )
    if "name" not in g.vertex_attributes ( ):
        g.vs["name"] = [str (i) for i in range (g.vcount ( ))]
    degrees = g.degree ( )
    betweenness = g.betweenness ( )
    closeness = g.closeness ( )
    if not g.is_directed ( ):
        clustering_coef = g.transitivity_local_undirected ( )
    print ("LOCAL MEASURES")
    for i in range (g.vcount ( )):
        print (g.vs["twitter_id"][i] + ':')
        print (" Degree:", degrees[i])
        print (" Betweenness:", betweenness[i])
        print (" Closeness:", closeness[i])
        if not g.is_directed ( ):
            print (" Clustering Coefficient:", clustering_coef[i])
    print ("Vertex with highest degree:", g.vs.select (_degree=g.maxdegree ( ))['name'])
    print ("Vertex with highest betweenness:", g.vs.select (_betweenness=max (betweenness))['name'])
    print ("Vertex with highest closeness:", g.vs.select (_closeness=max (closeness))['name'])
    if not g.is_directed ( ):
        print ("Vertex with highest clustering coefficient:",
               g.vs[clustering_coef.index (max (clustering_coef))]['name'])
    u.print_delta ("get local metrics ")


def get_max_vertex(g: Graph, mode_in_out_all):
    # degree OUT
    u.start_time ( )
    degrees = g.degree (mode=mode_in_out_all)  # .vs.degree(mode=igraph.OUT)
    max_deg = max (degrees)
    print ('found max degree OUT : ', max_deg)
    df_degree_out = [g.vs[idx] for idx, eb in enumerate (degrees) if eb == max_deg]
    print ('out max degree id : ', df_degree_out[0]["name"], ' twitter_id : ', df_degree_out[0]["twitter_id"],
           ' degree : ', max_deg)
    u.print_delta ("get max  degree ")
    return u.get_twitter_profile (df_degree_out[0]["twitter_id"])


# eg.dist <- degree_distribution(net, cumulative=T, mode="all") plot( x=0:max(deg), y=1-deg.dist, pch=19, cex=1.2, col="orange",
#      xlab="Degree", ylab="Cumulative Frequency")


def get_top_n_for_list(g: Graph, result_list, top_n: int):
    top = sorted (zip (g.vs, result_list), reverse=True)[:top_n]
    print ([node["twitter_id"] for node, _ in top])

    return top


def get_top_n_for_page_rank(g: Graph, directed: bool, top_n: int):
    u.start_time ( )
    top = get_top_n_for_list (g, g.pagerank (directed=directed), top_n)
    u.print_delta ('get top ' + str (top_n) + '  PageRank ')
    return top


def get_top_n_for_degree(g: Graph, mode_in_out_all, top_n: int):
    u.start_time ( )
    top = get_top_n_for_list (g, g.degree (mode=mode_in_out_all), top_n)
    u.print_delta ('get top ' + str (top_n) + '  Degree ')
    return top


def richclub(graph, fraction=0.1, highest=True, scores=None, indices_only=False):
    # from http://igraph.wikidot.com/python-recipes#toc6
    """Extracts the "rich club" of the given graph, i.e. the subgraph spanned
    between vertices having the top X% of some score.

    Scores are given by the vertex degrees by default.

    @param graph:    the graph to work on
    @param fraction: the fraction of vertices to extract; must be between 0 and 1.
    @param highest:  whether to extract the subgraph spanned by the highest or
                     lowest scores.
    @param scores:   the scores themselves. C{None} uses the vertex degrees.
    @param indices_only: whether to return the vertex indices only (and not the
                         subgraph)
    """

    if scores is None:
        scores = graph.degree ( )
    n = int (round (graph.vcount ( ) * fraction))
    indices = range (graph.vcount ( ))
    indices = sorted (indices, key=scores.__getitem__)
    # indices.sort (key=scores.__getitem__)
    # indices = sorted (zip (graph.vs, graph.degree (mode=ALL)), reverse=True)#get_top_n_for_list (graph, graph.degree (mode=ALL), n)

    if highest:
        indices = indices[-n:]
    else:
        indices = indices[:n]

    if indices_only:
        return indices

    return graph.subgraph (indices)


def authorities(g: Graph):
    return g.authority_score ( )


def hubs(g: Graph):
    return g.hub_score ( )
