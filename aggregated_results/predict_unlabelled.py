#!/bin/python

import sys
import random
import string
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction import DictVectorizer

#read in raw data from file and return a list of (label, article) tuples
def get_data(filename): return [line.strip().split('\t') for line in open(filename).readlines()]

#this is the main function you care about; pack all the cleverest features you can think of into here.
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
	dv = DictVectorizer(sparse=True) #You should change this to sparse=True before doing step 6, unless your computer has an eff-ton of memory... 
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

def predict_unlabelled(clf, X, outfile, text) : 
	num_articles = X.shape[0]
	for i,x in enumerate(X) : 
		outfile.write('%d\t%s'%(clf.predict(x)[0], text))

if __name__ == '__main__' : 

	#The program expects 2 arguments, a file containing training data and a file containing unlabelled data. 
	#If it does not get two arguments, print instructions and exit
	if len(sys.argv) < 3 : print "Usage: python classifier.py TRAINING_DATA UNLABELLED_DATA [n]"; exit(0)
	#Optionally, specify a number of lines of unlabelled data to predict
	n = None if len(sys.argv) < 4 else int(sys.argv[3])
	
	#Load the training data and then unseen data
	sys.stderr.write("Reading raw data\n")
	training_data = get_data(sys.argv[1])
	
	sys.stderr.write("Loading training data\n")
	#Convert training data into a label vector y and a feature matrix X
	y, X, texts, dv, le = get_matricies(training_data)

	sys.stderr.write("Training classifier\n")
	#Train your classifer on all the data you have
	clf = train_classifier(X,y) 
	
	sys.stderr.write("Loading unlabelled data\n")
	
	outfile = open("classifier_predictions.txt", 'w')
	with open(sys.argv[2]) as f : 
		sys.stderr.write("Predicting article")
		for i,text in enumerate(f) :
			if n and (i > n) : break 
			
			x, dv, le = get_matricies_for_unlabelled(text, dv, le)
			predict_unlabelled(clf, x, outfile, text)

	outfile.close()
	sys.stderr.write("Complete!!\n")


