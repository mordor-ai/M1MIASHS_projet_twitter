from igraph import *
import random

random.seed (1)

# from https://stackoverflow.com/questions/21976889/plotting-communities-with-python-igraph

g = Graph.Erdos_Renyi (30, 0.3)
comms = g.community_multilevel ( )

visual_style = {"edge_curved": False
    , "target": 'test_community.png'
    , "bbox": (1600, 1600)
    , "margin": 10

                }
plot (comms, mark_groups=True, **visual_style)
