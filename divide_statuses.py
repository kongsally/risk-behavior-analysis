import csv 

testing_userIDs = []
with open('testing_userID', 'r') as f:
	testing_userIDs = f.readlines()

training_userIDs = []
with open('training_userID', 'r') as f:
	training_userIDs = f.readlines()

testing_userIDs = [x.strip() for x in testing_userIDs]
training_userIDs = [x.strip() for x in training_userIDs]

print testing_userIDs
print '\n'
print training_userIDs

testing_csv = file('testing_data.csv', 'w')
training_csv = file('training_data.csv', 'w')

with open('data/statuses.csv', 'rb') as csvfile:
	status_reader = csv.reader(csvfile.read().splitlines())
	for row in status_reader:
		if row[1] in testing_userIDs:
			testing_csv.write(','.join(row) + '\n')
			#write this row on testing csv
		
		if row[1] in training_userIDs:
			# write this row on training csv
			training_csv.write(','.join(row) + '\n')