chunk = 10000000  # number of lines from the big file to put in small file
this_small_file = open('../files/split/twitter_0.csv', 'a')

with open('twitter_100M.csv') as file_to_read:
    for i, line in enumerate(file_to_read.readlines()):
        file_name = f'files/split/twitter_{i // chunk}.csv'
       # print(i, file_name)  # a bit of feedback that slows the process down a

        if file_name == this_small_file.name:
            this_small_file.write(line)

        else:
            this_small_file.write(line)
            this_small_file.close()
            this_small_file = open(f'{file_name}', 'a')