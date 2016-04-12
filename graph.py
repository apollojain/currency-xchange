from graphviz import Digraph

def create_dag(start, end, dictionary):
	print "gets here"
	f = Digraph(format='png')
	f.body.extend(['rankdir=LR', 'size="8,5"'])
	
	print "now here"
	f.attr('node', shape='doublecircle')
	f.node(start)
	f.node(end)

	f.attr('node', shape='circle')
	for cur1 in dictionary.keys():
		print cur1
		# if cur1 != start and cur1 != end:
		for cur2 in dictionary[cur1].keys():
			# if cur2 != start and cur2 != end: 
			print f
			f.edge(cur1, cur2, label=str(dictionary[cur1][cur2]))
# print "about to render"
	f.render('static/img/dag')


