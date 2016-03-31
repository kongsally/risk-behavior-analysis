#!/bin/python

import sys
import random
import string
import json

#read in raw data from file and return a list of (label, article) tuples
def get_data(filename): return [line.strip().split('\t') for line in open(filename).readlines()]

if __name__ == '__main__' : 

	#The program expects 2 arguments, a file containing training data and a file containing unlabelled data. 
	#If it does not get two arguments, print instructions and exit
	if len(sys.argv) < 3 : print "Usage: python classifier.py TRAINING_DATA UNLABELLED_DATA [n]"; exit(0)
	#Optionally, specify a number of lines of unlabelled data to predict
	n = None
	
	#Reading labeled testing data
	labeled_testing_data = get_data(sys.argv[1])
	
	#Loading labeled predicted data
	predicted_data = get_data(sys.argv[2])

	category = sys.argv[3]

	accuracy = {"true_positive": 0, "true_negative": 0, "false_positive": 0, "false_negative": 0}

	for i in xrange(len(labeled_testing_data)):
		test_label = labeled_testing_data[i][0]
		predicted_label = predicted_data[i][1]

		if test_label == "1":
			if test_label == predicted_label:
				accuracy["true_positive"] += 1
			else: 
				accuracy["false_negative"] += 1
		else:
			if test_label == predicted_label:
				accuracy["true_negative"] += 1
			else:
				accuracy["false_positive"] += 1

	sys.stderr.write('\n' + category + '\n')
	for x in accuracy:
		sys.stderr.write("%s\t%s\n"%(x, str(accuracy[x])))

	tp = float(accuracy["true_positive"])
	tn = float(accuracy["true_negative"])
	fp = float(accuracy["false_positive"])
	fn = float(accuracy["false_negative"])
	precision = round(tp / (tp + fp), 2)
	recall = round(tp / (tp + fn), 2)
	accuracy = round((tp + tn) / (tp + tn + fp + fn),2)

	sys.stderr.write("%s\t%s\n"%("Precision", str(precision)))
	sys.stderr.write("%s\t%s\n"%("Recall", str(recall)))
	sys.stderr.write("%s\t%s\n"%("Accuracy", str(accuracy)))

	with open(category + '_accuracy_count.json', 'w') as fp:
		json.dump(accuracy, fp)


