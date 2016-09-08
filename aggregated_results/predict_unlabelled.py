#!/bin/python

import sys
import random
import string
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction import DictVectorizer
from sklearn.cross_validation import train_test_split

#read in raw data from file and return a list of (label, article) tuples
def get_data(filename): return [line.strip().split('\t') for line in open(filename).readlines()]

#use the words as features
def get_features(X) : 
	features = []
	for x in X : 
		f = {}
		for w in [word.strip(string.punctuation) for word in x.split()] :
			if w not in f.keys() : 
				f[w] = 0
			f[w] += 1.0
		features.append(f)
	return features

#vectorize feature dictionaries and return feature and label matricies
def get_matricies(data) : 
	dv = DictVectorizer(sparse=True) 
	le = LabelEncoder()
	y = [d[0] for d in data]
	texts = [d[1] for d in data]
	X = get_features(texts)
	return le.fit_transform(y), dv.fit_transform(X), texts, dv, le

#vectorize feature dictionaries and return feature and label matricies
def get_matricies_for_unlabelled(text, dv, le) : 
	X = get_features([text])
	return dv.transform(X), dv, le

#train and multinomial naive bayes classifier
def train_classifier(X, y):
	clf = LogisticRegression()
	clf.fit(X,y)
	return clf 

#test the classifier
def test_classifier(clf, X, y):
	return clf.score(X,y)

def predict_unlabelled(clf, X, outfile, text) : 
	num_articles = X.shape[0]
	for i,x in enumerate(X) : 
		outfile.write('%f\t%d\t%s'%(max(clf.predict_proba(x)[0]),clf.predict(x),text))

#cross validation	
def cross_validate(X, y, dv=None, numfolds=10):
	test_accs = []
	split = 1.0 / numfolds
	for i in range(numfolds):
		x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=split, random_state=i)
		clf = train_classifier(x_train, y_train)
		test_acc = test_classifier(clf, x_test, y_test)
		test_accs.append(test_acc)
		print 'Fold %d : %.05f'%(i,test_acc)
	test_average = float(sum(test_accs))/ numfolds
	print 'Test Average : %.05f'%(test_average)
	return test_average

if __name__ == '__main__' : 

	#The program expects 3 arguments:
	# 1) a file containing training data 
	# 2) a file containing unlabelled data. 
	# 3) name of the new file with predicted labels

	#If it does not get two arguments, print instructions and exit
	if len(sys.argv) < 3 : print "Usage: python classifier.py TRAINING_DATA UNLABELLED_DATA NEW_FILE_NAME"; exit(0)
	#Optionally, specify a number of lines of unlabelled data to predict
	
	#Load the training data and then unseen data
	sys.stderr.write("Reading raw data: " + sys.argv[1] + "\n")
	training_data = get_data(sys.argv[1])
	
	#Convert training data into a label vector y and a feature matrix X
	sys.stderr.write("Loading training data\n")
	y, X, texts, dv, le = get_matricies(training_data)

	sys.stderr.write("Cross Validation\n")
	cross_validate(X,y)

	#Train the classifer on the data
	sys.stderr.write("Training classifier\n")
	clf = train_classifier(X,y) 
	
	sys.stderr.write("Loading unlabelled data\n")

	new_file_name = sys.argv[3]
	
	outfile = open(new_file_name, 'w')
	with open(sys.argv[2]) as f : 
		sys.stderr.write("Predicting article")
		for i,text in enumerate(f) :
			if n and (i > n) : break 

			x, dv, le = get_matricies_for_unlabelled(text, dv, le)
			predict_unlabelled(clf, x, outfile, text)

	outfile.close()
	sys.stderr.write("Complete!!\n")


