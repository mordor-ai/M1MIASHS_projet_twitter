import twint
import pandas as pd
#c = twint.Config()
#c.Limit = 20
#c.Username = "e_pellegrin"
#
#c.Pandas = True
#twint.run.Search(c)
#user_df = twint.storage.panda.User_df
#user_df.head()

c = twint.Config()
c.Limit = 20
#c.Username = 'e_pellegrin'
c.User_id= @niradio
c.Pandas = True
#c.Hide_output = True
twint.run.Lookup(c)

#Tweets_df = twint.storage.panda.Tweets_df
#print(Tweets_df.head())
User_df =  twint.storage.panda.User_df
print(User_df.head())