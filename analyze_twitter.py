import igraph
import twint
import datetime
from utils import metrics as gm

def start_time():
    global tstart
    tstart = datetime.datetime.now()


def get_delta():
    global tstart
    tend = datetime.datetime.now()
    return tend - tstart

print('====== Profiling results =======')

start_time()

g = igraph.Graph.Read_Picklez(fname= "./files/twitter_100K_picklez")

delta1 = get_delta()
print('Time required to load graph: %(delta1)s' % locals())

start_time()
gm.summary(g)
delta1 = get_delta()
print('Time required to get summary graph: %(delta1)s' % locals())
start_time()
gm.report(g)

delta1 = get_delta()
print('Time required to get report graph: %(delta1)s' % locals())
#gm.degree_distribution_plot(g,'dg_distri',loglog=False)

#gm.plot_degree_distribution(g)
#dD = g.degree_distribution(bin_width=10)
#print(dD)


#print(g.degree_distribution().bins())


start_time()
geant  = gm.in_giant(g)
print(geant.vcount())
gm.global_metrics(geant)
delta1 = get_delta()
print('Time required to get giant compoent : %(delta1)s' % locals())



start_time()
degree = geant.vs.select(_degree = geant.maxdegree())["twitter_id"]
print(degree[0])
delta1 = get_delta()
print('Time required to get most import twitter acount : %(delta1)s' % locals())

#gm.global_metrics(g)
#gm.local_metrics(g)

start_time()

c = twint.Config()
c.User_id = degree[0]
c.Limit = 20
c.Pandas = True
#c.Hide_output = True
try:
    twint.run.Lookup(c)
    User_df = twint.storage.panda.User_df
    print(User_df.head())
except:
    print("twitter id not found  for id :" % degree[0])

delta1 = get_delta()
print('Time required to get  twitter acount onto twitter: %(delta1)s' % locals())
#start_time()

#deg_in = g.vs.degree(type="in")
#max_deg_in =  max(deg_in)
#list_deg_in = [g.es[idx].tuple for idx, e_di in enumerate(deg_in) if e_di == max_deg_in]
