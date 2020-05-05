import numpy as np
import pandas as pd
import igraph
import datetime


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


n_rows = 10000000
compressed=  True
tstart = None
tend = None


def start_time():
    global tstart
    tstart = datetime.datetime.now()


def get_delta():
    global tstart
    tend = datetime.datetime.now()
    return tend - tstart

print('====== Profiling results =======')
start_time()
# load the original graph csv
df_edges = pd.read_csv(
    "./files/twitter_100M.csv",
    header='infer',
    sep=' ',
    low_memory=False,
    dtype={'dest': np.int32, 'source': np.int32},
    nrows=n_rows
)
delta1 = get_delta()
print('Time required to load edges: %(delta1)s' % locals())
start_time()

# on charge tout les noeuds
df_nodes = pd.read_csv(
    "./files/twitter-2010-ids.csv",
    header='infer',
    sep=',',
    low_memory=False,
    dtype={'node_id': np.int32, 'twitter_id': np.int32},
    # nrows=100000,
    index_col='node_id'
)
delta2 = get_delta()

print("Dataframe loaded with " + str(len(df_edges)) + "rows.")
print('Time required to load nodes: %(delta2)s' % locals())
#print(df_edges.head())
#print(df_nodes.head())
start_time()
# chargement du graphe
g = igraph.Graph.TupleList(df_edges.itertuples(index=False), directed=True, weights=False)
delta2 = get_delta()
print("graph loaded")
print('Time required to load graph: %(delta2)s' % locals())
print("loading nodes twiter ids")
# remplissage des caracteristiques

start_time()


for v in g.vs:
    # print(v['name'])
    index_num = v['name']
    try:
        v["twitter_id"] = df_nodes.loc[index_num, 'twitter_id']

    # print(v["twitter_id"])
    except KeyError:
        print('not found fo node id : ', index_num)
delta3 = get_delta()
print("Time required to add twitter ids: %(delta3)s" % locals())
start_time()
igraph.summary(g)
delta3 = get_delta()
print("Time required to get summary of graph : %(delta3)s" % locals())
file_name: str = './files/twitter_' + human_format(n_rows) + '_pickle'+  ('z' if compressed else '')
print("now saving graph to ", file_name)
start_time()
if compressed:
    g.write_picklez(file_name)
else:
    g.write_pickle(file_name)
print("graph saved")
delta4 = get_delta()
print("Time required to save pickle file: %(delta4)s" % locals())
print("====== End of program =======")

# igraph.Graph.DictList()
