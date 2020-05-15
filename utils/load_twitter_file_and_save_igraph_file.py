import utils as u

e_filename_csv = "../files/twitter_100M.csv"
n_filename_csv = "../files/twitter-2010-ids.csv"
folder_out = "../files/pickle/"
# u.load_twitter_and_save_pickle_graph(e_filename_csv,n_filename_csv,100,True,out_folder=folder_out)
# u.load_twitter_and_save_pickle_graph(e_filename_csv,n_filename_csv,1000,True,out_folder=folder_out)
# u.load_twitter_and_save_pickle_graph(e_filename_csv,n_filename_csv,10000,True,out_folder=folder_out)
# u.load_twitter_and_save_pickle_graph(e_filename_csv,n_filename_csv,100000,True,out_folder=folder_out)
# u.load_twitter_and_save_pickle_graph(e_filename_csv,n_filename_csv,1000000,True,out_folder=folder_out)
# u.load_twitter_and_save_pickle_graph(e_filename_csv,n_filename_csv,10000000,True,out_folder=folder_out)
u.load_twitter_and_save_pickle_graph (e_filename_csv, n_filename_csv, 50000000, True, out_folder=folder_out)

print ("====== End of program =======")
