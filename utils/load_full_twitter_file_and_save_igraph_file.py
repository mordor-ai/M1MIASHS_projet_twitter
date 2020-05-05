import numpy as np
import pandas as pd
import igraph
import datetime
import twint


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


n_rows = 10000000
compressed = True
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
    "../files/twitter_100M.csv",
    header='infer',
    sep=' ',
    low_memory=False,
    dtype={'source': np.int32, 'target': np.int32}
     #,nrows=n_rows
)
# on renome les colonnes
df_edges.columns = ['source', 'target']
delta1 = get_delta()
print('Time required to load edges: %(delta1)s' % locals())
start_time()

# on charge tout les noeuds
df_nodes = pd.read_csv(
    "../files/twitter-2010-ids.csv",
    header='infer',
    sep=',',
    low_memory=False,
    dtype={'node_id': np.int32, 'twitter_id': np.int32}
    #, nrows = n_rows
    #,index_col='node_id'
)
delta2 = get_delta()

print("Dataframe loaded with " + str(len(df_edges)) + "rows.")
print('Time required to load nodes: %(delta2)s' % locals())
print(df_edges.head())
print(df_nodes.head())
#print(df_nodes.to_dict('records'))
#print(df_edges.to_dict('records'))
print("Now loading graph")
start_time()
# chargement du graphe
g = igraph.Graph.DictList(df_nodes.to_dict('records')
                          , df_edges.to_dict('records')
                          , directed=True
                          , vertex_name_attr='node_id'
                          , edge_foreign_keys=('source', 'target')
                          #, iterative=False
                          )
delta2 = get_delta()
print("graph loaded")
print('Time required to load graph: %(delta2)s' % locals())
print("loading graph summary")

start_time()
igraph.summary(g)
delta1 = get_delta()
print('Time required to get summary graph: %(delta1)s' % locals())

# start_time()
# degrees_in = g.degree(mode="in")
# max_deg_in = max(degrees_in)
# print(max_deg_in)
# df_degree_in = [g.vs[idx].attributes() for idx, eb in enumerate(degrees_in) if eb == max_deg_in]
# print(df_degree_in)
# print(" twitter id  having max degree IN: ", df_degree_in)
# delta1 = get_delta()
# print('Time required to get  graph degree in : %(delta1)s' % locals())
#
#
# start_time()
# degrees_out = g.degree(mode="out")
# max_deg_out = max(degrees_out)
# print(max_deg_out)
# df_degree_out = [g.vs[idx].attributes() for idx, eb in enumerate(degrees_out) if eb == max_deg_out]
# print(df_degree_out)
# print(" twitter id  having max degree OUT: ", df_degree_out)
# delta1 = get_delta()
# print('Time required to get  graph degree out : %(delta1)s' % locals())




file_name: str = '../files/twitter_' + human_format(n_rows) + '_pickle'+  ('z' if compressed else '')
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

