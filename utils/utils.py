import datetime
import twint
import pandas as pd
import numpy as np
from igraph import *

tstart = None
tend = None


def start_time():
    global tstart
    tstart = datetime.datetime.now()


def get_delta():
    global tstart
    tend = datetime.datetime.now()
    return tend - tstart


def print_delta(myText: object) -> object:
    delta1 = get_delta()
    print('Time required to process {p}: {t}s'.format(p=myText, t=delta1, local=locals()))
    return delta1


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def get_twitter_profile(twitter_id):
    start_time()
    c = twint.Config()
    c.User_id = twitter_id
    c.Limit = 20
    c.Pandas = True
    # c.Hide_output = True
    try:
        # twint.run.Lookup(c)
        twint.run.Profile()
        User_df = twint.storage.panda.User_df
        print(User_df.head())
        print_delta("to get  twitter account onto twitter")
        return User_df
    except:
        print("twitter id not found  for id :", twitter_id)
        return


def load_twitter_and_save_pickle_graph(edge_file_name: str, node_file_name: str, n_rows: int = 1000000,
                                       is_compressed=True,
                                       out_folder: str = "./files/pickle/"):
    """

    :type n_rows: object
    """
    start_time()
    # load the original graph csv
    if n_rows>0:
       df_edges = pd.read_csv(
        edge_file_name,
        header='infer',
        sep=' ',
        low_memory=False,
        nrows=n_rows
        )
       file_name: str = out_folder + 'twitter_' + human_format(n_rows) + '_pickle' + ('z' if is_compressed else '')

    else:
       df_edges = pd.read_csv(
           edge_file_name,
           header='infer',
           sep=' ',
           low_memory=False
       )
       file_name: str = out_folder + 'twitter_100M_pickle' + ('z' if is_compressed else '')

    print_delta("load edges")
    # on renomme les colonnes car les données de following sont inversées
    df_edges.columns = ['target', 'source']
    start_time()

    # on charge tout les noeuds
    df_nodes = pd.read_csv(
        node_file_name,
        header='infer',
        sep=',',
        low_memory=False,
        dtype={'node_id': np.int32, 'twitter_id': np.int32}
        ,        index_col='node_id'
    )

    print("Dataframe loaded with " + str(len(df_edges)) + "rows.")
    print_delta("load nodes")

    start_time()
    # chargement du graphe
    g = Graph.TupleList(df_edges.itertuples(index=False), directed=True, weights=False)
    print_delta("load graph")
    print("graph loaded")

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
    print_delta("add twitter ids")
    print("now saving graph to ", file_name)
    start_time()
    if is_compressed:
        g.write_picklez(file_name)
    else:
        g.write_pickle(file_name)
    print("graph saved")
    print_delta("save pickle file")


def load_graph(n_rows: int, compressed: bool):
    start_time()
    file_name: str = './files/pickle/twitter_' + human_format(n_rows) + '_pickle' + ('z' if compressed else '')
    print("now loading graph from ", file_name)
    try:
        g = Graph.Read_Picklez(fname=file_name)

    except:
        print("Something goes wrong loading ", file_name)
        g = None
    finally:
        print_delta("load graph")
        return g
