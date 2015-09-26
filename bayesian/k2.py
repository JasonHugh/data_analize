# -*- coding:utf-8 -*-
import MySQLdb,sys
reload(sys)
sys.setdefaultencoding('utf-8')
db = MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',charset='utf8')
cursor = db.cursor()
sql = 'select cate_name,male_num,famale_num from cate order by cate_name'
result = cursor.execute(sql)
cates = cursor.fetchmany(result)

def get_k2(cate_name,male_num,famale_num):
	a = float(male_num)
	b = float(famale_num)
	c = float(10576-male_num)
	d = float(3423 - famale_num)
	#if a<5 or b<5 or c<5 or d<5:
	#	return 0
	k2 = 13999*(a*d-b*c)*(a*d-b*c)/((a+b)*(c+d)*(a+c)*(b+d))
	return k2

for cate in cates:
	k2 = get_k2(cate[0],cate[1],cate[2])
	if k2 >= 10:
		sql = 'select male,famale from cate where cate_name="' + cate[0] + '"'
		result = cursor.execute(sql)
		data = cursor.fetchmany(result)[0]
		print cate[0] + ' ' +str(data[0]) + ' ' + str(data[1])






