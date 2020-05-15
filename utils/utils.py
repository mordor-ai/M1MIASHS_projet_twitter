import datetime
import twint
import pandas as pd
import numpy as np
from igraph import *

tstart = None
tend = None
folder_img: str = "./files/img/"
img_suffix: str = ".png"


def str_now():
    now = datetime.datetime.now ( )
    return now.strftime ("%Y-%m-%d %H:%M:%S")


# datetime.datetime.strptime(datetime.datetime.now ( ), '%Y-%m-%d HH:MM:SS')  # datetime.datetime.now().isoformat (timespec='minutes')

def format_file(folder: str = folder_img, file_name: str = "", img_suffix: str = img_suffix):
    return folder + str_now ( ) + "_" + file_name + img_suffix


def start_time():
    global tstart
    tstart = datetime.datetime.now ( )


def get_delta():
    global tstart
    tend = datetime.datetime.now ( )
    return tend - tstart


def print_delta(myText: object) -> object:
    delta1 = get_delta ( )
    print ('Time required to process {p}: {t}s'.format (p=myText, t=delta1, local=locals ( )))
    return delta1


def human_format(num):
    magnitude = 0
    while abs (num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def fill_vertex(v: Vertex):
    # 'name' 'username' 'bio' 'url' 'join_datetime' 'join_date'
    # 'join_time' 'tweets' 'location' 'following' 'followers' 'likes' 'media'
    # 'private' 'verified' 'avatar' 'background_image'

    df = get_twitter_profile (v["twitter_id"])
    if df:
        v["twitter_name"] = df.loc[0, "name"]
        v['username'] = df.loc[0, "username"]
        v['bio'] = df.loc[0, "bio"]
        v['url'] = df.loc[0, "url"]
        v['join_datetime'] = df.loc[0, "join_datetime"]
        v['join_date'] = df.loc[0, "join_date"]
        v['join_time'] = df.loc[0, "join_time"]
        v['tweets'] = df.loc[0, "tweets"]
        v['location'] = df.loc[0, "location"]
        v['following'] = df.loc[0, "following"]
        v['followers'] = df.loc[0, "followers"]
        v['likes'] = df.loc[0, "likes"]
        v['media'] = df.loc[0, "media"]
        v['private'] = df.loc[0, "private"]
        v['verified'] = df.loc[0, "verified"]
        v['avatar'] = df.loc[0, "avatar"]
        v['background_image'] = df.loc[0, "background_image"]
    return v


def get_twitter_profile(twitter_id):
    start_time ( )
    c = twint.Config ( )
    c.User_id = twitter_id
    c.Limit = 20
    c.Pandas = True
    # c.Hide_output = True
    try:
        twint.run.Lookup (c)
        # twint.run.Profile ( )
        User_df: pd.DataFrame = twint.storage.panda.User_df
        print (User_df.head ( ))
        print (User_df.loc[0, "name"])
        print_delta ("to get  twitter account onto twitter")

        return User_df
    except:
        print ("twitter id not found  for id :", twitter_id)
        return


def load_twitter_graph(edge_file_name: str,
                       node_file_name: str,
                       n_rows: int = 1000000):
    start_time ( )
    # [TODO]:faire un truc
    # load the original graph csv
    if n_rows > 0:
        df_edges = pd.read_csv (
            edge_file_name,
            header='infer',
            sep=' ',
            low_memory=True,
            nrows=n_rows
        )

    else:
        df_edges = pd.read_csv (
            edge_file_name,
            header='infer',
            sep=' ',
            low_memory=True
        )

    print_delta ("load edges")
    # on renomme les colonnes car les données de following sont inversées
    df_edges.columns = ['target', 'source']
    # permet de réorganiser l'ordre des colonnes
    df_edges = df_edges.reindex (columns=['source', 'target'])
    start_time ( )

    # on charge tout les noeuds
    df_nodes = pd.read_csv (
        node_file_name,
        header='infer',
        sep=',',
        low_memory=False,
        dtype={'node_id': np.int32, 'twitter_id': np.int32}
        , index_col='node_id'
    )

    print ("Dataframe loaded with " + str (len (df_edges)) + "rows.")
    print_delta ("load nodes")

    start_time ( )
    # chargement du graphe
    if (n_rows > 0):
        g = Graph.TupleList (df_edges.itertuples (index=False), directed=True, weights=False)
        print_delta ("load graph")
        print ("graph loaded")
        print ("loading nodes twiter ids")
        # remplissage des caracteristiques

        start_time ( )
        for v in g.vs:
            # print(v['name'])
            index_num = v['name']
            try:
                v["twitter_id"] = df_nodes.loc[index_num, 'twitter_id']

            # print(v["twitter_id"])
            except KeyError:
                print ('not found fo node id : ', index_num)
        print_delta ("add twitter ids")
    else:
        g = Graph.DictList (df_nodes.to_dict ('records')
                            , df_edges.to_dict ('records')
                            , directed=True
                            , vertex_name_attr='node_id'
                            , edge_foreign_keys=('source', 'target')
                            # , iterative=False
                            )
        print_delta ("load graph")
    return g


def load_twitter_and_save_pickle_graph(edge_file_name: str,
                                       node_file_name: str,
                                       n_rows: int = 1000000,
                                       is_compressed=True,
                                       out_folder: str = "./files/pickle/"):
    """

    :type n_rows: object
    """

    g = load_twitter_graph (edge_file_name, node_file_name, n_rows)
    file_name: str = out_folder + 'twitter_' + (human_format (n_rows) if (n_rows > 0) else '100M') + '_pickle' + (
        'z' if is_compressed else '')

    print ("now saving graph to ", file_name)
    start_time ( )
    if is_compressed:
        g.write_picklez (file_name)
    else:
        g.write_pickle (file_name)
    print ("graph saved")
    print_delta ("save pickle file")


def load_graph(n_rows: int, compressed: bool):
    start_time ( )
    file_name: str = './files/pickle/twitter_' + human_format (n_rows) + '_pickle' + ('z' if compressed else '')
    print ("now loading graph from ", file_name)
    try:
        g = Graph.Read_Picklez (fname=file_name)

    except:
        print ("Something goes wrong loading ", file_name)
        g = None
    finally:
        print_delta ("load graph")
        return g
