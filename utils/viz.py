import matplotlib.pyplot as plt
import seaborn as sns
from igraph import *
import numpy as np
from utils import utils as u
from utils import metrics as gm

folder_img: str = "./files/img/"
img_suffix: str = ".png"


def set_color_from_communities(g, communities):
    pal = drawing.colors.ClusterColoringPalette (len (communities))
    g.vs['color'] = pal.get_many (communities.membership)


def viz_graph(g: Graph, in_out, file_name, folder, layout, show_label_by_degree):
    u.start_time ( )
    # Define colors used for outdegree visualization
    colours = ['#fecc5c', '#a31a1c']
    outdegree = g.degree (mode=in_out)
    max_degree = max (outdegree)
    # Order vertices in bins based on outdegree
    bins = np.linspace (0, max_degree, len (colours))
    digitized_degrees = np.digitize (outdegree, bins)
    # file_name = folder_img + file_name + img_suffix
    my_layout = g.layout (layout=layout)
    visual_style = {  # Don't curve the edges
        "edge_curved": False
        # Scale vertices based on degree

        , "vertex_size": [x / max_degree * 10 + 1 for x in outdegree]  # outdegree * 10  #
        ,
        "vertex_label": [(v["twitter_id"] if ((1 - v.degree ( ) / max_degree) <= show_label_by_degree) else "") for v
                         in g.vs]
        , "vertex_label_size": [x / max_degree * 22 for x in outdegree]
        , "target": u.format_file (folder=folder, file_name=file_name, img_suffix=img_suffix)
        , "bbox": (1600, 1600)
        , "margin": 10
        , "layout": my_layout

    }
    # Set colors according to bins
    g.vs["color"] = [colours[x - 1] for x in digitized_degrees]
    # Also color the edges
    for ind, color in enumerate (g.vs["color"]):
        edges = g.es.select (_source=ind)
        edges["color"] = [color]
    # Plot the graph
    drawing.plot (g, **visual_style)
    u.print_delta ("generate viz graph ")


def viz_community(g: Graph, in_out, file_name: str, folder: str, community_type, show_label_by_degree_percent):
    u.start_time ( )
    max_degree = max (g.degree (mode=in_out))
    visual_style = {"edge_curved": False
        , "vertex_label": [
            (v["twitter_id"] if ((1 - v.degree ( ) / max_degree) <= show_label_by_degree_percent) else None) for v
            in g.vs]

        , "target": u.format_file (folder=folder, file_name=file_name, img_suffix=img_suffix)
        , "bbox": (1600, 1600)
        , "margin": 10

                    }
    g_undirected: Graph = g.as_undirected ( )
    communities = g_undirected.community_multilevel ( )
    # https://stackoverflow.com/questions/43580304/python-modularity-statistic-using-louvain-package#43583445
    modularity_score = g_undirected.modularity (communities.membership)

    print ("The modularity Q based on igraph is {}".format (modularity_score))
    # Community detection
    # communities = g.community_edge_betweenness (directed=False)

    # communities = geant.community_fastgreedy().as_clustering()
    # communities = geant.community_infomap().as_clustering()
    # clusters = communities.as_clustering()

    # Set edge weights based on communities
    # weights = {v: len(c) for c in clusters for v in c}
    # geant.es["weight"] = [weights[e.tuple[0]] + weights[e.tuple[1]] for e in geant.es]

    # Plot the graph
    drawing.plot (communities, mark_groups=True, **visual_style)
    u.print_delta ("generate community viz graph ")


def viz_hubs(g: Graph, in_out, file_name: str, folder: str):
    u.start_time ( )
    hubs = gm.hubs (g)
    my_layout = g.layout_auto ( )
    g.vs["hub_score"] = hubs
    visual_style = {"edge_curved": False, "vertex_label": [
        (v["twitter_id"] if (v["hub_score"] > 0) else "") for v
        in g.vs], "target": u.format_file (folder=folder, file_name=file_name, img_suffix=img_suffix),
                    "bbox": (1600, 1600), "margin": 10, "vertex_size": [x * 50 for x in hubs], "layout": my_layout}
    # Plot the graph
    drawing.plot (g, **visual_style)
    u.print_delta ("generate community viz graph ")


def viz_authorities(g: Graph, in_out, file_name: str, folder: str):
    u.start_time ( )
    auths = gm.authorities (g)
    g.vs["authority_score"] = auths
    my_layout = g.layout_auto ( )
    visual_style = {"edge_curved": False
        , "vertex_label": [
            (v["twitter_id"] if (v["authority_score"] > 0) else "") for v
            in g.vs]
        , "target": u.format_file (folder=folder, file_name=file_name, img_suffix=img_suffix)
        , "bbox": (1600, 1600)
        , "margin": 10
        , "vertex_size": [x * 50 for x in auths], "layout": my_layout

                    }

    # Plot the graph
    drawing.plot (g, **visual_style)
    u.print_delta ("generate community viz graph ")
