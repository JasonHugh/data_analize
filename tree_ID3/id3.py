# -*- coding:utf-8 -*-
import csv,math

class ID3:
	def __init__(self):
		self.train_data = self.get_train_data()
		#print train_data[0]['12520267']

	def train(self,train_data):
		tag_data = train_data[0]
		sex_data = train_data[1]
		tags = train_data[2]
	    classList = [sex_data[uid] for uid in sex_data]
	    if classList.count(classList[0]) == len(classList):
	        return classList[0]
	    if len(tag_data[0]) == 1:
	        return majorityCnt(classList)   
	    bestFeat = find_best_tag(train_data)
	    bestFeatLabel = tags[bestFeat][0]
	    myTree = {bestFeatLabel:{}}
	    del(tags[bestFeat])
	    featValues = [tag_data[uid][bestFeat] for uid in tag_data]
	    uniqueVals = set(featValues)
	    for value in uniqueVals:
	        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), tags)
	    return myTree

	def majorityCnt(classList):
	    classCount = {}
	    for vote in classList:
	        if vote not in classCount.key():
	            classCount[vote] = 0;
	        classCount[vote] += 1
	    sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)
	    return sortedClassCount[0][0]

	def find_best_tag(self,train_data):
		tag_data = train_data[0]
		sex_data = train_data[1]
		gains = []
		for i in range(len(self.tags)):
			tag_0 = 0  #某tag为0的条数
			tag_0_sex_0 = 0  #某tag为0&sex为0的条数
			tag_1 = 0
			tag_1_sex_0 = 0
			for uid in tag_data:
				if int(tag_data[uid][i]) == 0:
					tag_0 += 1
					if int(sex_data[uid]) == 0:
						tag_0_sex_0 += 1
				else:
					tag_1 += 1
					if int(sex_data[uid]) == 0:
						tag_1_sex_0 += 1
			e0 = self.get_entropy(tag_0,tag_0_sex_0)
			e1 = self.get_entropy(tag_1,tag_1_sex_0)
			#求信息增益
			tag_all = tag_0+tag_1
			gain = 1 - (float(tag_0)/float(tag_all))*e0 - (float(tag_1)/float(tag_all))*e1
			gains.append(gain)
		#返回信息熵最大的tag的下标
		print gains.index(max(gains))

	#求熵
	def get_entropy(self,num_all,num_sex_0):
		if num_all > 0:
			rate_0 = float(num_sex_0)/float(num_all)
			rate_1 = float(num_all - num_sex_0)/float(num_all)
			if rate_0 > 0 and rate_1 >0:
				e = -rate_0*math.log(2,rate_0)-rate_1*math.log(2,rate_1)
			else:
				e = 0
		else:
			e = 0
		return e

	def get_train_data(self):
		#获取训练数据，以一定格式返回
		tags = self.load_csv('cate_value.csv')
		dateset = self.load_csv('../bayesian/test_data.csv')
		tag_data = {}
		sex_data = {}
		for data in dateset:
			if tag_data.has_key(data[1]):
				tag_data[data[1]] += (data[2],)
			else:
				tag_data[data[1]] = (data[2],)
				sex_data[data[1]] = data[0]
		new_tag_data = {}
		for uid in tag_data:
			for tag in tags:
				try:
					list(tag_data[uid]).index(tag[0])
					if new_tag_data.has_key(uid):
						new_tag_data[uid] += (1,)
					else:
						new_tag_data[uid] = (1,)
				except:
					if new_tag_data.has_key(uid):
						new_tag_data[uid] += (0,)
					else:
						new_tag_data[uid] = (0,)
		return new_tag_data,sex_data,tags

	def load_csv(self,filename):
		lines = csv.reader(open(filename, "rb"))
		dataset = list(lines)
		return dataset

id3 = ID3()
id3.find_best_split()