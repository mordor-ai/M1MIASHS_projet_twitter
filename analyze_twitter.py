import igraph
import twint
import datetime

def start_time():
    global tstart
    tstart = datetime.datetime.now()


def get_delta():
    global tstart
    tend = datetime.datetime.now()
    return tend - tstart

print('====== Profiling results =======')

start_time()

g = igraph.Graph.Read_Picklez(fname= "./files/twitter_100M_pickle")

delta1 = get_delta()
print('Time required to load graph: %(delta1)s' % locals())

start_time()
igraph.summary(g)
delta1 = get_delta()
print('Time required to get summary graph: %(delta1)s' % locals())
start_time()
degree = g.vs.select(_degree = g.maxdegree())["twitter_id"]

print(degree[0])
delta1 = get_delta()
print('Time required to get most import twitter acount : %(delta1)s' % locals())
start_time()

c = twint.Config()
c.User_id = degree[0]
c.Limit = 20
c.Pandas = True
#c.Hide_output = True
twint.run.Lookup(c)
User_df =  twint.storage.panda.User_df
print(User_df.head())
delta1 = get_delta()
print('Time required to get  twitter acount onto twitter: %(delta1)s' % locals())
#start_time()

#deg_in = g.vs.degree(type="in")
#max_deg_in =  max(deg_in)
#list_deg_in = [g.es[idx].tuple for idx, e_di in enumerate(deg_in) if e_di == max_deg_in]
