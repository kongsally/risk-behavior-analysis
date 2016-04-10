#!/bin/python

import os
import sys
import string
import random
import operator
import predict_unlabelled

#read in raw data from file and return a list of (label, article) tuples
def get_data(filename): return [line.strip().split('\t') for line in open(filename).readlines()]

def predict_bootsrap(training_data):
	print len(training_data)

	predictions = []
	
	sys.stderr.write("Loading training data\n")
	#Convert training data into a label vector y and a feature matrix X
	y, X, texts, dv, le = predict_unlabelled.get_matricies(training_data)

	sys.stderr.write("Training classifier\n")
	#Train your classifer on all the data you have
	clf = predict_unlabelled.train_classifier(X,y) 
	
	sys.stderr.write("Loading unlabelled data\n")
	
	with open(sys.argv[2]) as f : 
		sys.stderr.write("Predicting article\n")
		for i,text in enumerate(f) :
			
			x, dv, le = predict_unlabelled.get_matricies_for_unlabelled(text, dv, le)
			predict_unlabelled.predict_unlabelled(clf, x, predictions, text)

	predicted_statuses = [line[1] for line in training_data]
	for line in predictions:
		if len(line) > 2 and float(line[0]) > 0.95 and line[2] not in predicted_statuses:
			training_data.append([str(line[1][0]), line[2]])

	print len(training_data)

if __name__ == '__main__' :

	# first argument = training data
	# second argument = unlabelled training data
	# third argument = number of iterations

	#Load the training data and then unseen data
	sys.stderr.write("Reading raw data\n")
	training_data = get_data(sys.argv[1])
	iterations = int(sys.argv[3])


	for i in xrange(iterations):
		predict_bootsrap(training_data)

	bootstrapped_labels = open(str(iterations) + "_" + sys.argv[1], 'w')
	for line in training_data:
		bootstrapped_labels.write(line[0] + '\t' + line[1].strip() + '\n')

	
