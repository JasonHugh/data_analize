# -*- coding:utf-8 -*-
import csv,math,traceback
import matplotlib.pyplot as plt  
import numpy as np
from sklearn.metrics import roc_curve, auc
class Bayes:
	def __init__(self,train_file,test_file):
		self.male = {}
		self.famale = {}
		self.model = {}
		self.test_file = test_file
		filename = train_file
		dataset = self.loadCsv(filename)
		for data in dataset:
			self.male[data[0]] = data[1]
			self.famale[data[0]] = data[2]

		for tag in self.male.keys():
			if self.famale.has_key(tag):
				a = self.male[tag]
				b = self.famale[tag]
				c = float(a)/(float(a)+float(b))
				self.model[tag] = c
		self.test_data = self.get_test_data()

	def get_score(self,tags):
		score = 0
		a = 1
		b = 1

		for tag in tags :
			if self.model.has_key(tag):
				a *= float(self.model[tag])
				b *= float(1-self.model[tag])
		
		try:
			score = a / (a + b)
		except:
			score = 0

		return score

	def get_thresholds(self):
		thresholds = []
		tag_data = self.test_data[0]
		sex_data = self.test_data[1]
		for uid in tag_data:
			tags = tag_data[uid]
			sex = int(sex_data[uid])
			score = self.get_score(tags)
			thresholds.append([sex,score])
		return sorted(thresholds,key=lambda x:x[1],reverse=1)
	
	def predict(self,score,threshold):
		if float(score) > float(threshold):
			return 1
		else:
			return 0

	def test(self,threshold):
		tag_data = self.test_data[0]
		sex_data = self.test_data[1]
		tp = 0
		fp = 0
		tn = 0
		fn = 0
		for uid in tag_data:
			tags = tag_data[uid]
			sex = int(sex_data[uid])
			score = self.get_score(tags)
			if score == 0:
				continue
			predict = self.predict(score,threshold)
			if sex == 1:
				if predict == 1:
					tp +=1
				else:
					fn += 1
			else:
				if predict == 1:
					fp += 1
				else:
					tn += 1
		#计算fpr,tpr
		if tp == 0:
			tpr = 0
		else:
			tpr = float(tp) / float(tp+fn)
		if fp == 0:
			fpr = 0
		else:
			fpr = float(fp) / float(fp+tn)
		print fpr,tpr,threshold,tp,fp,tn,fn

		#precision = float(tp)/float(tp+fp)
		#recall = float(tp)/float(tp+fn)
		#fscore = (2*precision*recall)/(precision+recall)
		#print 'Precision:'+str(precision)
		#print 'Recall:'+str(recall)
		#print " F-score:"+str(fscore)
		print "Accuracy:" + str(float(tp+tn) / float(tp+tn+fp+fn))
		return fpr,tpr
	
	def get_roc(self,thresholds,color,label=''):
		x = []
		y = []
		for i in thresholds:
			fpr,tpr = self.test(i)
			x.append(fpr)
			y.append(tpr)
		label += ' auc=' + str(auc(np.array(x),np.array(y)))
		plt.plot(x,y,color,label=label)

	def get_image(self):
		plt.plot([0,1],[0,1],'c--')
		plt.xlabel('FPR')
		plt.ylabel('TPR')
		plt.xlim(0, 1)
		plt.ylim(0, 1)
		plt.title('ROC')
		plt.legend()
		plt.show()

	def get_test_data(self):
		tag_data = {}
		sex_data = {}
		filename = self.test_file
		dataset = self.loadCsv(filename)
		for data in dataset:
			if tag_data.has_key(data[1]):
				tag_data[data[1]] += (data[2],)
			else:
				tag_data[data[1]] = (data[2],)
				sex_data[data[1]] = data[0]
		return tag_data,sex_data

	def get_test_data_from_db(self):
		import MySQLdb
		db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="test",charset="utf8")
		cursor = db.cursor()
		sql = 'select uid,sex,pack_id from user_pack'
		result = cursor.execute(sql)
		user_pack = cursor.fetchmany(result)
		sql = 'select * from pack_cate'
		result = cursor.execute(sql)
		pack_cate = cursor.fetchmany(result)
		
		pack_dict = {}
		for p in pack_cate:
			if pack_dict.has_key(p[1]):
				pack_dict[p[1]] += (p[2],)
			else:
				pack_dict[p[1]] = (p[2],)
		
		sql = 'insert into test_data(sex,uid,cate_name) values(%s,%s,%s)'
		test_data = []
		for i,u in enumerate(user_pack):
			if pack_dict.has_key(u[2]):
				for p in pack_dict[u[2]]:
					test_data.append([u[1],u[0],p])
					try:
						cursor.execute(sql,(u[1],u[0],p))
						db.commit()
					except:
						traceback.print_exc()
				    	db.rollback()
			if i%100000 == 0:
				print 'write 100000'
		return test_data

	def loadCsv(self,filename):
		lines = csv.reader(open(filename, "rb"))
		dataset = list(lines)
		return dataset

thresholds = []
i = 0
while i <= 1:
	thresholds.append(i)
	i += 0.05
bayes = Bayes('train_data.csv','D:/HAY/Desktop/test_data.csv')
bayes6 = Bayes('train_data2.csv','D:/HAY/Desktop/test_data.csv')
#bayes1 = Bayes('train_data.csv','D:/HAY/Desktop/test_data_400_1.csv')
#bayes2 = Bayes('train_data.csv','D:/HAY/Desktop/test_data_400_2.csv')
#bayes3 = Bayes('train_data.csv','D:/HAY/Desktop/test_data_400_3.csv')
#bayes4 = Bayes('train_data.csv','D:/HAY/Desktop/test_data_400_4.csv')
#bayes5 = Bayes('train_data.csv','D:/HAY/Desktop/test_data_400_5.csv')
#bayes.test(0.5)
##bayes1.test(0.5)
bayes.get_roc(thresholds,'r',u'all tag')
bayes6.get_roc(thresholds,'r--',u'some tag')
#bayes1.get_roc(thresholds,'g',u'测试数据第1批400')
#bayes2.get_roc(thresholds,'b',u'测试数据第2批400')
#bayes3.get_roc(thresholds,'c',u'测试数据第3批400')
#bayes4.get_roc(thresholds,'m',u'测试数据第4批400')
#bayes5.get_roc(thresholds,'k',u'测试数据第5批400')
bayes.get_image()