# -*- coding:utf-8 -*-
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt  
import MySQLdb,math
import traceback,time
db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="test",charset="utf8")
cursor = db.cursor()
sql = 'select cate_name,user_num,male-famale imbus from cate'
exc = cursor.execute(sql)
cates = cursor.fetchmany(exc)
plt.figure(figsize=(15,15))
plt.title(u'类型关系图')
G = nx.Graph()
def draw_nodes(start,end,color):
	male_nodes = [cate[0] for cate in cates if float(cate[2]) > float(start) and float(cate[2]) <= float(end)]
	G.add_nodes_from(male_nodes)
	pos = nx.random_layout(G)
	nx.draw_networkx_nodes(G,node_size = 200,pos = pos,nodelist =male_nodes,node_color=color)
	nx.draw_networkx_labels(G,pos = pos)
draw_nodes(0,0.01,'#63B7EE')
draw_nodes(0.01,0.03,'#6381EE')
draw_nodes(0.03,0.05,'#6363EE')
draw_nodes(0.05,1,'#0018B2')

draw_nodes(-1,-0.08,'#C80202')
draw_nodes(-0.08,-0.05,'#F34040')
draw_nodes(-0.05,-0.02,'#F57777')
draw_nodes(-0.02,0,'#FADDDD')
#关系
sql = 'select cate1,cate2,relation from cate_relation'
exc = cursor.execute(sql)
rows = cursor.fetchmany(exc)
for row in rows:
	G.add_edge(row[0],row[1])
	G.add_weighted_edges_from([(row[0],row[1],row[2])])
pos = nx.random_layout(G)
nx.draw_networkx_edges(G,pos)
plt.show()