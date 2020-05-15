import matplotlib.pyplot as plt
import seaborn as sns
from igraph import *
import numpy as np
from utils import utils as u
from utils import metrics as gm
from numpy import interp

folder_img: str = "./files/img/"
img_suffix: str = ".png"


def set_color_from_communities(g, communities):
    pal = drawing.colors.ClusterColoringPalette (len (communities))
    g.vs['color'] = pal.get_many (communities.membership)


def viz_graph(g: Graph, degree, file_name: str, folder: str, layout: str = "auto", show_label_by_degree: int = 0.1,
              label: str = "twitter_id", ):
    u.start_time ( )
    # Define colors used for outdegree visualization
    colours = ['#fecc5c', '#a31a1c']

    max_degree = max (degree)
    if type (max_degree) == int:
        if max_degree >= 1:
            num_colors = (max_degree) + 1
            # https://github.com/igraph/python-igraph/issues/98
            palette = RainbowPalette (n=num_colors)
            color_list = [palette.get (d) for d in degree]
            # Set colors according to bins
            g.vs["color"] = color_list  # [colours[x - 1] for x in digitized_degrees]

    # Order vertices in bins based on outdegree
    bins = np.linspace (0, max_degree, len (colours))
    digitized_degrees = np.digitize (degree, bins)
    # file_name = folder_img + file_name + img_suffix
    my_layout = g.layout (layout=layout)
    visual_style = {  # Don't curve the edges
        "edge_curved": False
        # Scale vertices based on degree

        , "vertex_size": [x / max_degree * 50 + 1 for x in degree]  # outdegree * 10  #
        ,
        # https://github.com/igraph/python-igraph/issues/98
        "vertex_label": [v["twitter_name"] if v["twitter_name"] != "" else (
            v[label] if ((1 - v.degree ( ) / max_degree) <= show_label_by_degree) else "")
                         for v in g.vs]
        , "vertex_label_size": [x / max_degree * 22 for x in degree]
        , "target": u.format_file (folder=folder, file_name=file_name, img_suffix=img_suffix)
        , "bbox": (1600, 1600)
        , "margin": 10
        , "layout": my_layout

    }

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
    my_layout = g.layout_auto ( )
    visual_style = {"edge_curved": False
        , "vertex_label": [
            # (v["twitter_id"] if ((1 - v.degree ( ) / max_degree) <= show_label_by_degree_percent) else None)
            v["twitter_name"] if v["twitter_name"] != "" else (
                v["twitter_id"] if ((1 - v.degree ( ) / max_degree) <= show_label_by_degree_percent) else None)
            for v in g.vs]

        , "target": u.format_file (folder=folder, file_name=file_name, img_suffix=img_suffix)
        , "bbox": (1600, 1600)
        , "margin": 10
        , "layout": my_layout

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
    visual_style = {"edge_curved": False, "vertex_label": [v["twitter_name"] if v["twitter_name"] != "" else
                                                           (v["twitter_id"] if (v["hub_score"] > 0) else "") for v
                                                           in g.vs],
                    "target": u.format_file (folder=folder, file_name=file_name, img_suffix=img_suffix),
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
        , "vertex_label": [v["twitter_name"] if v["twitter_name"] != "" else
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


def viz_diameter(g: Graph, file_name: str, folder: str):
    u.start_time ( )
    is_directed = g.is_directed ( )
    diam = g.get_diameter (is_directed)

    # Define colors used for outdegree visualization
    colours = ['#CCCCCC', "#FFCC66"]
    for i in range (len (g.vs)):
        g.vs[i]["color"] = colours[0]
    for v in g.vs.select (diam):
        v["color"] = colours[1]
    # g.vs.select()["color"] = [colours[1] for x in diam]
    for i in range (len (g.es)):
        g.es[i]["color"] = colours[0]
    for eid in g.get_eids (path=diam, directed=is_directed):
        g.es[eid]["color"] = colours[1]

    g.vs.select (diam)["belongs_to_diameter"] = 1
    my_layout = g.layout_auto ( )
    visual_style = {"edge_curved": False
        , "vertex_label": [
            (v["twitter_id"] if (v["belongs_to_diameter"] == 1) else "") for v
            in g.vs]
        , "target": u.format_file (folder=folder, file_name=file_name, img_suffix=img_suffix)
        , "bbox": (1600, 1600)
        , "margin": 10
        , "vertex_color": g.vs["color"]
        , "edge_color": g.es["color"]
                    # , "vertex_size": [x * 50 for x in auths], "layout": my_layout

                    }

    # Plot the graph
    drawing.plot (g, **visual_style)
    u.print_delta ("generate community viz graph ")
