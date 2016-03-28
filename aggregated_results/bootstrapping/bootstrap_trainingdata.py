#!/bin/python

import os
import sys
import string
import random
import operator

#read in raw data from file and return a list of (label, article) tuples
def get_data(filename): return [line.strip().split('\t') for line in open(filename).readlines()]


if __name__ == '__main__' :
	new_prediction = get_data(sys.argv[1])
	old_prediction = get_data(sys.argv[2])
	predicted_statuses = [line[1] for line in old_prediction]

	for line in new_prediction:
		if len(line) > 3 and float(line[0]) > 0.9 and line[2] not in predicted_statuses:
			print '%d\t%s'%(int(line[1]), line[2])
