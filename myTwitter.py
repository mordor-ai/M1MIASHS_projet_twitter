
#projet reseaux sociaux
# analyse du reseau twitter
# Emmanuel Pellegrin
# copyrights 2020
import numpy as np
import pandas as pd
from graph_tool.all import *



def read_file(fname){


# Import du fichier
from google.colab import files
uploaded = files.upload()
df = pd.read_csv(fname, usecols=['Source', 'Target'],
 dtype={'Source': np.int32, 'Target': np.int32},sep=' ')

}
def build_graph(dataframe, method){
    g = Graph(directed=True)
    ##g.add_edge_list(
}

def import_build_neo4j_graph(){}



    graph = Graph()

    tx = graph.cypher.begin()
    files = [file for file in os.listdir("data/profiles") if file.endswith("json")]
    for file in files:
        with open("data/profiles/{0}".format(file), "r") as file:
            profile = json.loads(file.read())
            print profile["screen_name"]

            params = {
                "twitterId" : profile["id"],
                "screenName": profile["screen_name"],
                "name": profile["name"],
                "description": profile["description"],
                "followers" : profile["followers"],
                "friends" : profile["friends"]
            }
            statement = """
                        MERGE (p:Person {twitterId: {twitterId}})
                        REMOVE p:Shadow
                        SET p.screenName = {screenName},
                            p.description = {description},
                            p.name = {name}
                        WITH p

                        FOREACH(followerId IN {followers} |
                          MERGE (follower:Person {twitterId: followerId})
                          ON CREATE SET follower:Shadow
                          MERGE (follower)-[:FOLLOWS]->(p)
                        )

                        FOREACH(friendId IN {friends} |
                          MERGE (friend:Person {twitterId: friendId})
                          ON CREATE SET friend:Shadow
                          MERGE (p)-[:FOLLOWS]->(friend)
                        )
                        """
            tx.append(statement, params)

            tx.process()
    tx.commit()

def main(argv = None){
    parser = argparse.ArgumentParser(description='This is my twitter graph analyzer program')
# specific user
    parser.add_argument('--import_profiles-into-neo4j')
    parser.add_argument('--download-tweets')
    parser.add_argument('--download-profile')
    parser.add_argument('--read-user')
    if argv is None:
        argv = sys.argv

    args = parser.parse_args()

    if args.import_profiles_into_neo4j:
        import_profiles_into_neo4j()
    return
}x



# Lecture du fichier
fname ='twitter_100M-ids.csv'