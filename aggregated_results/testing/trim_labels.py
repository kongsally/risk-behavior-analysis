#!/bin/python

import sys
import random
import string
import json

#read in raw data from file and return a list of (label, article) tuples
def get_data(filename): return [line.strip().split('\t') for line in open(filename).readlines()]

if __name__ == '__main__' : 


	#Reading labeled testing data
	labeled_testing_data = get_data(sys.argv[1])
	
	statuses = {}

	for i in xrange(len(labeled_testing_data)):
		try:
			label = labeled_testing_data[i][0]
			status = labeled_testing_data[i][2]
			if label not in statuses:
				statuses[label] = []
			statuses[label].append(status)
		except:
			continue

	trimmed_negatives = []
	trimmed_positives = []

	if len(statuses["1"]) * 2 > len(statuses["0"]):
		trimmed_negatives = statuses["0"]
		trimmed_positives = statuses["1"]
	else:
		trimmed_negatives = random.sample(set(statuses["0"]), len(statuses["1"]) * 2)
		trimmed_positives = statuses["1"]

	sys.stderr.write("1: " + str(len(trimmed_positives)) + '\n')
	sys.stderr.write("0: " + str(len(trimmed_negatives)) + '\n')

	trimmed_label = open(sys.argv[2], 'w')

	for status in trimmed_positives:
		trimmed_label.write("1" + '\t' + status + '\n')

	for status in trimmed_negatives:
		trimmed_label.write("0" + '\t' + status + '\n')


