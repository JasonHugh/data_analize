# -*- coding:utf-8 -*-
import csv
class Bayes:
	def __init__(self):
		self.male = {}
		self.famale = {}
		self.model = {}
		filename = 'male_cate.csv'
		dataset = self.loadCsv(filename)
		for data in dataset:
			self.male[data[0]] = data[1]
		filename = 'famale_cate.csv'
		dataset = self.loadCsv(filename)
		for data in dataset:
			self.famale[data[0]] = data[1]

		for tag in self.male.keys():
			if self.famale.has_key(tag):
				a = self.male[tag]
				b = self.famale[tag]
				c = float(a)/(float(a)+float(b))
				self.model[tag] = c

	def predict(self,tags,p):
		predic = 0
		a = 1
		b = 1
		
		for tag in tags :
			if self.model.has_key(tag):
				a *= float(self.model[tag])
				b *= float(1 - self.model[tag])
		if a+b == 0:
			predic = 0
		else:
			predic = a/(a + b)
		
		if predic > p:
			return 1
		else:
			return 0

	def test(self,test_data,sex):
		right = 0
		for uid in test_data:
			tags = test_data[uid]
			if sex == self.predict(tags,0.15):
				right += 1
			else:
				print '判断错误用户：' + uid
		print "判断正确的用户数："+str(right)
		print "正确率为:" + str(float(right) / float(len(test_data)))

	def run(self):
		test_data = self.get_test_data()
		self.test(test_data,1)

	def get_test_data(self):
		test_data = {}
		filename = '50male.csv'
		dataset = self.loadCsv(filename)
		for data in dataset:
			if test_data.has_key(data[0]):
				test_data[data[0]] += (data[1],)
			else:
				test_data[data[0]] = (data[1],)
		return test_data

	def loadCsv(self,filename):
		lines = csv.reader(open(filename, "rb"))
		dataset = list(lines)
		return dataset


bayes = Bayes()
bayes.run()