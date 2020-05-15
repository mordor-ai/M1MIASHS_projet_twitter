import twint
import pandas as pd

# c = twint.Config()
# c.Limit = 20
# c.Username = "e_pellegrin"
#
# c.Pandas = True
# twint.run.Search(c)
# user_df = twint.storage.panda.User_df
# user_df.head()

c = twint.Config ( )
# c.Limit = 20
c.Username = 'twitter'
# c.User_id= @niradio
c.Pandas = True
c.Store_object = True
c.Hide_output = False
c.Debug = True
c.Output
twint.run.Lookup (c)
# twint.run.Profile (c )
# twint.output.
# Tweets_df = twint.storage.panda.Tweets_df
# print(Tweets_df.head())
User_df: pd.DataFrame = twint.storage.panda.User_df
print (User_df)
print (User_df.columns.values)
print (User_df.loc[0, "name"])  # renvoie emmanuel pellegrin
# nemarche pas
users = twint.output.users_list
print (users[0].join_date)

print (" ####### END OF PROGRAM ########")
