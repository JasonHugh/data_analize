# -*- coding:utf-8 -*-
import csv,math
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

	def predict(self,tags,threshold):
		predic = 0
		a = 0
		b = 0

		for tag in tags :
			if self.model.has_key(tag):
				a += math.log(float(self.model[tag]),math.e)
				b += math.log(float(1-self.model[tag]),math.e)
		
		try:
			predic = math.exp(a) / (math.exp(a) + math.exp(b))
		except:
			predic = 0

		if predic > threshold:
			return 1
		else:
			return 0

	def test(self,test_data):
		tag_data = test_data[0]
		sex_data = test_data[1]
		right = 0
		for uid in tag_data:
			tags = tag_data[uid]
			sex = sex_data[uid]
			if int(sex) == self.predict(tags,0.5):
				right += 1
			else:
				print sex,uid
		print "判断正确的用户数："+str(right)
		print "正确率为:" + str(float(right) / float(len(tag_data)))

	def run(self):
		test_data = self.get_test_data()
		self.test(test_data)

	def get_test_data(self):
		tag_data = {}
		sex_data = {}
		filename = '100ren.csv'
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


bayes = Bayes()
bayes.run()