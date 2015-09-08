# -*- coding:utf-8 -*-
import csv,math
import matplotlib.pyplot as plt  
import numpy as np
class Bayes:
	def __init__(self):
		self.male = {}
		self.famale = {}
		self.model = {}
		filename = 'cate_value1.csv'
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
		print fpr,tpr,threshold
		#print "TPR:"+str(float(tp) / float(tp+fn))
		#print "FPR:"+str(float(fp) / float(fp+tn))
		#print "判断正确的用户数："+str(tp+tn)
		#print "正确率为:" + str(float(tp+tn) / float(tp+tn+fp+fn))

	def get_test_data(self):
		tag_data = {}
		sex_data = {}
		filename = 'D:/HAY/Desktop/test_data.csv'
		dataset = self.loadCsv(filename)
		for data in dataset:
			if tag_data.has_key(data[1]):
				tag_data[data[1]] += (data[2],)
			else:
				tag_data[data[1]] = (data[2],)
				sex_data[data[1]] = data[0]
		return tag_data,sex_data

	def loadCsv(self,filename):
		lines = csv.reader(open(filename, "rb"))
		dataset = list(lines)
		return dataset

'''
bayes = Bayes()
#bayes.test(0.5)
#thresholds = bayes.get_thresholds()
#for t in thresholds:
#	bayes.test(t[1])
i = 0
while i <= 1:
	bayes.test(i)
	i += 0.1
'''
plt.plot([0,1],[0,1],'c--')
lines = csv.reader(open('roc.csv', "rb"))
dataset = list(lines)
x = [i[0] for i in dataset]
y = [i[1] for i in dataset]
plt.plot(x,y)
lines = csv.reader(open('roc1.csv', "rb"))
dataset = list(lines)
x = [i[0] for i in dataset]
y = [i[1] for i in dataset]
plt.plot(x,y,'r')
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.title('ROC')
plt.legend()
plt.show()
