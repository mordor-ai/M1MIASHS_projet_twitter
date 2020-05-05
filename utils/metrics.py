# -*- coding: utf-8 -*-

"""
igraphplus.metrics
~~~~~~~~~~~~~~~~~

This module contains the metrics for graphs.
"""
import matplotlib.pyplot as plt
import seaborn as sns
from igraph import *


def efficiency(g: Graph, initial=0, removed=0):
    """Efficiency calculation"""
    result = 0.0
    paths = g.shortest_paths()
    if g.is_directed():
        for path in paths:
            for distance in path:
                if 0 < distance < float('Inf'):
                    result += float(1) / distance
    else:
        for index, path in enumerate(paths):
            for distance in path[index + 1:]:
                if 0 < distance < float('Inf'):
                    result += float(2) / distance

    n = g.vcount()
    if initial:
        n = initial
    if removed:
        n -= removed

    result /= n * (n - 1)
    return result


def degree_distribution(g: Graph):
    """ bin = [min_i, max_i, amount)"""
    distribution = {}
    for b in g.degree_distribution().bins():
        if b[2]:
            distribution[b[0]] = b[2]
    return distribution


def plot_degree_distribution(g: Graph):
    plt.figure()
    plt.hist(g.degree())
    plt.xlabel("Degree")
    plt.ylabel("#Vertices")
    plt.show()


def degree_distribution_plot(g: Graph, filename='degree_distribution', loglog=True, marker='.'):
    import pylab

    f = g.degree_distribution(bin_width=1)
    xs, ys = zip(*[(left, count) for left, _, count in
                   g.degree_distribution().bins()])
    # pylab.bar(xs, ys)
    pylab.show()
    if loglog:
        pylab.xscale('log')
        pylab.yscale('log')
    pylab.xlabel('k')
    pylab.ylabel('N')
    pylab.title('Degree distribution')
    # pylab.plot(xs, ys, marker)
    pylab.plot(f.keys(), f.values(), marker)
    pylab.savefig(filename + '.png')


def degree_properties(g: Graph):
    """ Response with min, max, average degree and it's std"""
    import numpy

    degrees = numpy.array(g.degree())
    min_degree = degrees.min()
    max_degree = degrees.max()
    mean_degree = degrees.mean()
    std_degree = degrees.std()
    return min_degree, max_degree, mean_degree, std_degree


def summary(g: Graph):
    degree_stats = degree_properties(g)
    connected = 'connected' if (g.is_connected()) else 'unconnected'
    directed = 'directed' if (g.is_directed()) else 'undirected'
    deg = '(%d, %0.2f ± %0.2f, %d)' % (degree_stats[0], degree_stats[2], degree_stats[3], degree_stats[1])
    return 'N:%d E:%d %s %s Components:%d Degree:%s' % (
        g.vcount(), g.ecount(), connected, directed, len(g.components()), deg)


def report(g: Graph):
    degree_stats = degree_properties(g)
    print('Graph is: %s, %s' %
          ('Connected' if (g.is_connected()) else 'Disconnected', 'Directed' if (g.is_directed()) else 'Undirected'))
    print('Number of nodes: %d' % g.vcount())
    print('Number of edges: %d' % g.ecount())
    print('Number of components: %d' % len(g.components()))
    print('Degree: min = %d, max = %d, mean = %0.2f, std = %0.2f' % (
        degree_stats[0], degree_stats[1], degree_stats[2], degree_stats[3]))


# from  https://stackoverflow.com/questions/25147163/identity-of-nodes-in-the-giant-component-in-igraph-with-python
def in_giant(g: Graph):
    largest = g.clusters().giant()
    return largest


def global_metrics(g: Graph):
    summary(g)
    print("GLOBAL MEASUURES")
    print("Connected:", g.is_connected())
    print("Density:", g.density())
    print("Diameter:", g.diameter())
    print("Clustering Coefficient:", g.transitivity_undirected())
    print("Average Local Clustering Coefficient:", g.transitivity_avglocal_undirected())
    print("Average Degree:", mean(g.degree()))
    print("Max Degree:", g.maxdegree())
    print("Average Betweenness:", mean(g.betweenness()))
    print("Max Betweenness:", max(g.betweenness()))
    print("Average Closeness:", mean(g.closeness()))
    print("Max Closeness:", max(g.closeness()))


def local_metrics(g: Graph):
    if "name" not in g.vertex_attributes():
        g.vs["name"] = [str(i) for i in range(g.vcount())]
    degrees = g.degree()
    betweenness = g.betweenness()
    closeness = g.closeness()
    if not g.is_directed():
        clustering_coef = g.transitivity_local_undirected()
    print("LOCAL MEASURES")
    for i in range(g.vcount()):
        print(g.vs["twitter_id"][i] + ':')
        print(" Degree:", degrees[i])
        print(" Betweenness:", betweenness[i])
        print(" Closeness:", closeness[i])
        if not g.is_directed():
            print(" Clustering Coefficient:", clustering_coef[i])
    print("Vertex with highest degree:", g.vs.select(_degree=g.maxdegree())['name'])
    print("Vertex with highest betweenness:", g.vs.select(_betweenness=max(betweenness))['name'])
    print("Vertex with highest closeness:", g.vs.select(_closeness=max(closeness))['name'])
    if not g.is_directed():
        print("Vertex with highest clustering coefficient:", g.vs[clustering_coef.index(max(clustering_coef))]['name'])
