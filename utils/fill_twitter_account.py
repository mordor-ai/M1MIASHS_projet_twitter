from utils import utils as u
import pandas as pd
import numpy as np

folder_out = "../files/"

# on charge tout les noeuds
df_nodes: pd.DataFrame = pd.read_csv (
    u.n_filename_csv,
    header='infer',
    sep=',',
    low_memory=True,
    dtype={'node_id': np.int32, 'twitter_id': np.int32}
    , index_col='node_id'
)

for row in df_nodes.rows:
    u.fill_vertex (v=row)

df_nodes.to_csv (folder_out + "rich_" + u.n_filename_csv)
