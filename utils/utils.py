import datetime
import twint

tstart = None
tend = None


def start_time():
    global tstart
    tstart = datetime.datetime.now()


def get_delta():
    global tstart
    tend = datetime.datetime.now()
    return tend - tstart


def print_delta(myText):
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
        print("twitter id not found  for id :" , twitter_id)
        return

