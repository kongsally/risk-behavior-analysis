import random

user_freq = {}
freq_tiers = [0, 10, 100, 500, 1000, 3000]
freq_user = {}
for x in freq_tiers:
	freq_user[x] = []

user_ids = []

with open('user_freq', 'r') as f:
	lines = f.readlines()
	for line in lines:
		entry = line.split('\t')
		user_ids.append(entry[0])
		user_freq[entry[0]] = entry[1]

		for x in xrange(len(freq_tiers)-1, -1, -1):
			if int(entry[1]) > freq_tiers[x]:
				freq_user[freq_tiers[x]].append(entry[0])
				break

testing_data = {}
training_data = {}

for x in freq_user:
	length = len(freq_user[x])
	rand_user1 = random.choice(freq_user[x])
	freq_user[x].remove(rand_user1)
	rand_user2 = random.choice(freq_user[x])
	freq_user[x].remove(rand_user2)

	testing_data[rand_user1] = user_freq[rand_user1]
	testing_data[rand_user2] = user_freq[rand_user2]

	for y in freq_user[x]:
		training_data[y] = user_freq[y]

testing_sum = 0
for i in testing_data.keys():
	print i + ": " + str(user_freq[i])
	testing_sum += int(user_freq[i])

print "Total testing data: " + str(testing_sum)

testing_data_users = file('testing_userID', 'w')
training_data_users = file('training_userID', 'w')

for i in testing_data.keys():
	testing_data_users.write(i + '\n')

for i in training_data.keys():
	training_data_users.write(i + '\n')

testing_data_users.close()
training_data_users.close()



