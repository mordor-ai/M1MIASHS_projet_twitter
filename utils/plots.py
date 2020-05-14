import matplotlib.pyplot as plt
from igraph import *
from utils import utils as u
from collections import Counter
from operator import itemgetter




def autolabel(rects):
    for rect in rects:
        height = rect.get_height ( )
        plt.text (rect.get_x ( ) + rect.get_width ( ) / 2., 1.04 * height, '%s' % float (height))


def plot_plot_degree_distribution(g: Graph, file_name='degree_distribution', loglog=True, marker='.',
                                  folder: str = u.folder_img):
    import pylab
    u.start_time ( )
    f = g.degree_distribution (bin_width=1)
    xs, ys = zip (*[(left, count) for left, _, count in
                    g.degree_distribution ( ).bins ( )])
    # pylab.bar(xs, ys)
    pylab.show ( )
    if loglog:
        pylab.xscale ('log')
        pylab.yscale ('log')
    pylab.xlabel ('k')
    pylab.ylabel ('N')
    pylab.title ('Degree distribution')
    pylab.plot (xs, ys, marker)
    # pylab.plot(f.keys(), f.values(), marker)

    pylab.savefig (u.format_file (folder=folder, file_name=file_name))
    u.print_delta (' generate  degree_distribution_plot')


def plot_scatter_frequency_degree_distribution(g: Graph, modeInOutAll, file_name: str, folder: str = u.folder_img):
    # from  https://stackoverflow.com/questions/53958700/plotting-degree-distribution-of-networkx-digraph-using-networkx-degree-histogram
    from collections import Counter
    from operator import itemgetter

    # G = some networkx graph

    degrees = g.degree (mode=modeInOutAll)
    degree_counts = Counter (degrees)
    x, y = zip (*degree_counts.items ( ))

    plt.figure (1)

    # prep axes
    plt.xlabel ('degree')
    plt.xscale ('log')
    plt.xlim (1, max (x))

    plt.ylabel ('frequency')
    plt.yscale ('log')
    plt.ylim (1, max (y))
    # do plot
    plt.scatter (x, y, marker='.')

    plt.savefig (u.format_file (folder=folder, file_name=file_name))
    plt.show ( )


def plot_histo_degree_distribution(g: Graph, modeInOutAll, isLog: bool = True,
                                   file_name: str = "",
                                   folder: str = u.folder_img):
    b = g.degree_distribution (bin_width=1)
    # print('degree histogram', b)
    a = []
    a = g.degree (mode=modeInOutAll)
    rect = plt.hist (a, bins=range (0, (max (a))), density=1, stacked='True', facecolor='b')
    plt.xlabel ('Number of Nodes')
    plt.ylabel ('Degree')
    if (isLog):
        plt.xscale ('log')
        plt.yscale ('log')
    plt.title ('Degree Distribution')
    #
    print ('figure is saved ')

    plt.savefig (u.format_file (folder=folder, file_name=file_name))
    plt.show ( )


def plot_histo_components_distribution(cl_list: VertexClustering, isLog: bool = True,
                                       file_name: str = "", folder: str = u.folder_img):
    cl_sizes = cl_list.sizes ( )
    sorted_cl_sizes = sorted (cl_sizes, reverse=True)
    plt.xlabel ('Number of Nodes')
    plt.ylabel ('Cluster')
    plt.title ('Components Distribution')
    if (isLog):
        plt.xscale ('log')
        plt.yscale ('log')
    rect = plt.hist (sorted_cl_sizes, bins=range (0, (max (sorted_cl_sizes))), density=1, stacked='True', facecolor='b')
    print ('figure is saved ')
    plt.savefig (u.format_file (folder=folder, file_name=file_name))
    plt.show ( )


def plot_bar_components_distribution(cl_list: VertexClustering, isLog: bool = True,
                                     file_name: str = "", folder: str = u.folder_img):
    cl_sizes = cl_list.sizes ( )
    sorted_cl_sizes = sorted (cl_sizes, reverse=True)
    plt.xlabel ('Number of Nodes')
    plt.ylabel ('Cluster')
    plt.title ('Components Distribution')
    if (isLog):
        plt.xscale ('log')
        plt.yscale ('log')
    rect = plt.bar (range (len (sorted_cl_sizes)), sorted_cl_sizes, color='red')
    autolabel (rect)
    print ('figure is saved ')
    plt.savefig (u.format_file (folder=folder, file_name=file_name))
    plt.show ( )
