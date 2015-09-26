# -*- coding:utf-8 -*-
import csv,math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt 
from sklearn import tree
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import train_test_split

class ID3:
	#def __init__(self):
		#self.train_data,self.tags = self.format_train_data()
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

	def format_data(self,filename):
		#获取训练数据，以一定格式返回
		dataSet = self.load_csv(filename)
		train_data = {}
		sex_data = {}
		tags = self.get_tags()
		for data in dataSet:
			if train_data.has_key(data[1]):
				train_data[data[1]] += (data[2],)
			else:
				train_data[data[1]] = (data[2],)
				sex_data[data[1]] = data[0]
		new_train_data = {}
		for uid in train_data:
			for tag in tags:
				try:
					list(train_data[uid]).index(tag)
					if new_train_data.has_key(uid):
						new_train_data[uid] += (1,)
					else:
						new_train_data[uid] = (1,)
				except:
					if new_train_data.has_key(uid):
						new_train_data[uid] += (0,)
					else:
						new_train_data[uid] = (0,)
			new_train_data[uid] += (sex_data[uid],)
		return new_train_data

	def data_to_csv(self,filename,data):
		writer = csv.writer(open(filename,'wb'))
		for uid in tag_data:
			writer.writerow(tag_data[uid])

	def get_tags(self):
		dataSet = self.load_csv('all_tag.csv')
		tags = [data[0] for data in dataSet]
		return tags

	def load_csv(self,filename):
		lines = csv.reader(open(filename, "rb"))
		dataset = list(lines)
		return dataset

	def get_data_from_csv(self,filename):
		data  = []
		labels = []
		dataSet = self.load_csv(filename)
		for d in dataSet:
			data.append(d[:-1])
			labels.append(float(d[-1]))
		return np.array(data),np.array(labels)

	def sklearn_test(self):
		''' 训练数据读入 '''
		x,y = self.get_data_from_csv('test_data.csv')
		''' 拆分训练数据与测试数据 '''
		x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
		''' 使用信息熵作为划分标准，对决策树进行训练 '''
		clf = tree.DecisionTreeClassifier(criterion='gini')
		clf.fit(x_train, y_train)

		#''' 把决策树结构写入文件 '''
		#with open("tree.dot", 'w') as f:
		#  f = tree.export_graphviz(clf, out_file=f)
		 
		#''' 系数反映每个特征的影响力。越大表示该特征在分类中起到的作用越大 '''
		#print(clf.feature_importances_)
		#
		'''测试结果的打印'''
		#answer = clf.predict(x_train)
		#print(x_train)
		#print(answer)
		#print(y_train)
		#print(np.mean( answer == y_train))
		#
		'''准确率与召回率'''
		#precision, recall, thresholds = precision_recall_curve(y_train, clf.predict(x_train))
		
		answer = clf.predict_proba(x_test)[:,1]
		fpr, tpr, thresholds = roc_curve(y_test, answer)
		print fpr
		roc_auc = auc(fpr, tpr)
		plt.plot(fpr, tpr)

		print(classification_report(y_test, answer, target_names = ['famale', 'male']))

	def get_image(self):
		plt.plot([0,1],[0,1],'c--')
		plt.xlabel('FPR')
		plt.ylabel('TPR')
		plt.xlim(0, 1)
		plt.ylim(0, 1)
		plt.title('ROC')
		plt.legend()
		plt.show()



id3 = ID3()
id3.sklearn_test()
#id3.get_image()