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
     ,nrows=n_rows
)
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
    , nrows = n_rows
    #,index_col='node_id'
)
delta2 = get_delta()

print("Dataframe loaded with " + str(len(df_edges)) + "rows.")
print('Time required to load nodes: %(delta2)s' % locals())
print(df_edges.head())
print(df_nodes.head())
print(df_nodes.to_dict('records'))
print(df_edges.to_dict('records'))
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
print("loading nodes twiter ids")

start_time()
igraph.summary(g)
delta1 = get_delta()
print('Time required to get summary graph: %(delta1)s' % locals())
start_time()
degree = g.vs.select(_degree=g.maxdegree())["twitter_id"]

print(degree[0])
delta1 = get_delta()
print('Time required to get most import twitter acount : %(delta1)s' % locals())
start_time()

c = twint.Config()
c.User_id = degree[0]
c.Limit = 20
c.Pandas = True
# c.Hide_output = True
twint.run.Lookup(c)
User_df = twint.storage.panda.User_df
print(User_df.head())
delta1 = get_delta()
print('Time required to get  twitter acount onto twitter: %(delta1)s' % locals())
