import matplotlib.pyplot as plt
from igraph import *
import sys
import os

# for plotting tool and file must be in a same location


l = os.listdir (os.getcwd ( ))
if 'temp' not in l:
	os.mkdir ('temp')
else:
	pass

if sys.argv[1] == True or '-h' or '-H' or '--help':
	print ('	usage -format [filename]' + '\n')
	print (
		'	format: adjacencncy matrix -adj  edgelist -edgelist  graphml -graphml  lgl -lgl  random network - random' + '\n')
else:
	sys.argv[1] == None or False
	print ('	usage -format [filename]')

if sys.argv[1] == '-adj':
	g = Graph.Read_Adjacency (sys.argv[2])
	print ('No. of nodes in given file ', len (g.vs))
	layout = g.layout ('kk')
	plot (g, layout=layout)


elif sys.argv[1] == '-edgelist':
	g = Graph.Read_Ncol (sys.argv[2], names=True, weights="if_present", directed=True)
	print ('No. of nodes in given file ', len (g.vs))
	a = []
	a = g.degree ( )
	c = []
	for i in range (len (g.vs)):
		c.append (str (i))
	g.vs['label'] = c
	layout = g.layout ('kk')
	plot (g, layout=layout)


elif sys.argv[1] == '-graphml':
	g = Graph.Read_GraphML (sys.argv[2])
	print ('No. of nodes in given file ', len (g.vs))
	layout = g.layout ('kk')
	plot (g, layout=layout)


elif sys.argv[1] == '-adj':
	g = Graph.Read_ (sys.argv[2])
	print ('No. of nodes in given file ', len (g.vs))
	layout = g.layout_sphere ('kk')
	plot (g, layout=layout)


elif sys.argv[1] == '-lgl':
	g = Graph.Read_Lgl, (sys.argv[2])
	print ('No. of nodes in given file ', len (g.vs))
	layout = g.layout ('kk')
	plot (g, layout=layout)


elif sys.argv[1] == '-random':
	num = input ("Enter the number of nodes ")
	g = Graph.GRG (num, 0.1)
	c = []
	for i in range (num):
		c.append (str (i))
	g.vs['label'] = c
	a = []
	a = g.degree ( )
	layout = g.layout ('kk')
	plot (g, target='graph_with_nodes' + str (num) + '.png', layout=layout)

print ('\n' + '	=========== parameters covered ============')
print ('	Histogram...............................(1)')
print ('	Centrality : ')
print ('		*Eigenvector centrality.........(2)')
print ('		*Betweenness centrality.........(3)')
print ('	Average path length.....................(4)')
print ('	Degree distribution.....................(5)')
print ('	Clustering coefficient..................(6)')
print ('	Shortest path between two nodes.........(7)')
print ('	Shortest path between all nodes.........(8)')
print ('	Degree distribution power law...........(9)')
print ('	Functional motifs......................(10)')
print ('	Neighbour vertex : ')
print ('		* for two specified vertes.....(11)')
print ('		* for all vertex of graph......(12)')
print ('	Modularity.............................(13)')
print ('	connectivity : ')
print ('		vertex *for given two vertex...(14)')
print ('	       	       *overall................(15)')
print ('		Edge   *for given two vertex...(16)')
print ('	       	       *overall................(17)')
print ('	No. of clusters........................(18)')
print ('	Adjacency matrix.......................(19)')
print ('	given node id its EC no(for enzyme data file)..(20)')
print ('	EC no for all node ids(for enzyme data file)...(21)')
print ('	Edgelist...............................(22)')
print ('	Diameter...............................(23)')
print ('	Average path length....................(24)')
print ('	giant_component........................(25)')
print ('	add vertex(single)..............  ..   (26)')
print ('	add vertices(many)..................   (27)')
print ('	delete vertex(single)................ .(28)')
print ('	delete vertices(many).... ........... .(29)')
print ('	maximum degree nodes.... ........... . (30)')
print ('	minimum degree nodes.... ...........  .(31)')
print ('	Deleting all nodes saving in file .....(32)' + '\n')

user = int (input ('Type the no of function wanted: '))

if user == 1:
	b = g.degree_distribution (bin_width=1)
	print ('degree histogram', b)
	a = []
	a = g.degree ( )
	plt.hist (a, bins=range (0, (max (a))), normed=1, stacked='True', facecolor='b')
	plt.xlabel ('Number of Nodes')
	plt.ylabel ('Degree')
	plt.title ('Degree Distribution')
	plt.show ( )
	print ('figure is saved ')
	plt.savefig ("hist.png")

if user == 5:
	c = []
	for i in range (len (g.vs)):
		c.append (str (i))
	g.vs['label'] = c
	a = []
	a = g.degree ( )
	degree = open ('degree_distribution.txt', 'w')
	for deg in range (len (c)):
		degree.write ('degree vertex id' + '\t' + str (a[deg]) + '\t' + str (c[deg]) + '\n')
	print ('degree distribution (degree, vertex id) file is saved degree_distribution.txt')

if user == 7:
	start = input (
		"Enter the name(which is integer here) of the node from which the shortest path is to be calculated : ")
	end = input ("Enter the name(which is integer here) of the node to which the shortest path is to be calculated : ")
	print ('shortest path', g.get_all_shortest_paths (start, to=end, weights=None, mode=OUT))
if user == 8:
	print ('shortest path', g.shortest_paths (source=None, target=None, weights=None, mode=ALL))
if user == 6:
	print ('clustering coefficient', g.transitivity_undirected (mode='nan'))

if user == 3:
	startc = input ("Enter the start node from which betweenness centrality to be calculated : ")
	endc = input ("Enter the end node till which betweenness centrality to be calculated :  ")
	print ('betweenness centrality', g.betweenness (startc, endc))
if user == 2:
	print ('eigenvector centrality',
		   g.eigenvector_centrality (directed=True, scale=True, weights=None, return_eigenvalue=False))
if user == 9:
	deg = g.Static_Power_Law (len (g.vs), 10, exponent_out=2, exponent_in=-1, loops=False, multiple=False,
							  finite_size_correction=True)
	plot (deg)
	print ('Degree distribution(power law)', deg)
if user == 4:
	print ('average path length', g.average_path_length (directed=False, unconn=True))
if user == 10:
	print (' no. of functional motif ', g.motifs_randesu_no (size=3, cut_prob=None, ))
if user == 12:
	print ('neighbourhood vertice for each', g.neighborhood (vertices=None, order=1, mode=ALL))
if user == 11:
	neighbors = input ('type the vertics to whom neighbour vertex needed: ')
	print ('neighbour vertices to gien vertices', g.neighbors (neighbors, mode=ALL))
if user == 13:
	membership = a
	print ('modularity', g.modularity (membership, weights=None))
if user == 14:
	x = input ('connectivity from: ')
	y = input ('connectivity to : ')
	print ('connectivity from one node to another',
		   g.vertex_connectivity (source=x, target=y, checks=True, neighbors="error"))
if user == 15:
	print ('vertex connectivity overall', g.vertex_connectivity (source=-1, target=-1, checks=True, neighbors="error"))
if user == 16:
	source = input ('source vertex : ')
	target = input ('target vertex : ')
	print ('edge connectivity ', g.edge_connectivity (source=source, target=target, checks=True))
if user == 17:
	print ('overall connectivity', g.edge_connectivity (source=-1, target=-1, checks=True))
if user == 19:
	g.get_adjacency (type=GET_ADJACENCY_BOTH, eids=True)
	g.write_adjacency ('matrix.txt')
	print ('adjacency matrix saved in file ')

if user == 18:
	print ('no of clusters of the graph', len (g.clusters (mode=STRONG)))
if user == 20:
	node = input ('type the node id : ')
	print (g.vs[node])
if user == 21:
	for i in range (len (g.vs)):
		print (i, g.vs[i])
if user == 22:
	edgelist = g.get_adjedgelist (mode=OUT)
	fout = open ("edgelist.txt", 'w')
	fout.write (str (edgelist))
	print ("edgelist saved")
	fout.close ( )
if user == 23:
	print ('Diameter is ', g.diameter (directed=True, unconn=True, weights=None))

if user == 24:
	print (g.average_path_length (directed=False, unconn=True))
if user == 25:
	print (g.clusters ( ).giant ( ).write_graphml ("gaint_component.graphml"))
	print ('gaint component is saved in graphml file')

if user == 26:
	n = input (' single vertex to be added attribute:  ')
	g.add_vertex (n)
	print (g.write_graphml ("new_added_single_node.graphml"))
	print ('new added vertice is saved in graphml file ')

if user == 27:
	n = input ('the number of vertices to be added, :  ')
	g.add_vertices (n)
	g.write_graphml ("new_added_many_node.graphml")
	print ('new added vertice is saved in graphml file ')

if user == 28:
	dlt = input ('id of vertices to be deleted:  ')
	g.delete_vertices (dlt)
	g.write_graphml ("new_deleted__node.graphml")
	print ('Deleted vertex FILE is graphml file ')

# if user == 29:
# 	s =raw_input('ids of vertices to be deleted saprated by space:  ')
# 	dlt_list=list(map(int, s.split()))
# 	g.delete_vertices(dlt_list)
# 	g.write_graphml("new_deleted__node.graphml")
# 	print ('Deleted vertex FILE is graphml file ')


if user == 30:
	a = g.degree ( )
	print ('node with max degree', max (a), g.vs (max (a)))

if user == 31:
	a = g.degree ( )
	print ('node with max degree', min (a), g.vs (max (a)))

if user == 32:
	num = 0
	j = 0
	while num == 0:
		g.delete_vertices (0)
		if len (g.vs) == 1:
			break
		g.write_edgelist (str (os.getcwd ( )) + "/temp/deleted_node_" + str (j) + ".txt")
		print ('files complete and saved after deleting node :- ', str (j))
		j += 1
