import utils as u

e_filename_csv= "./files/twitter_100M.csv"
n_filename_csv="./files/twitter-2010-ids.csv"

#u.load_twitter_and_save_pickle_graph(e_filename_csv,n_filename_csv,100,True)
#u.load_twitter_and_save_pickle_graph(e_filename_csv,n_filename_csv,1000,True)
#u.load_twitter_and_save_pickle_graph(e_filename_csv,n_filename_csv,10000,True)
#u.load_twitter_and_save_pickle_graph(e_filename_csv,n_filename_csv,100000,True)
#u.load_twitter_and_save_pickle_graph(e_filename_csv,n_filename_csv,1000000,True)
u.load_twitter_and_save_pickle_graph(e_filename_csv,n_filename_csv,100000000,True)

print("====== End of program =======")


