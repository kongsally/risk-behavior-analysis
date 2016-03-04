import csv
import json
import status_reader
import string

def load_anew_dict():
	anew = {}
	for line in open('BRM-emot-submit.csv'):
		entry = line.split(",")
		anew[entry[1]] = [entry[2], entry[5], entry[8]]
	return anew

def user_words(statuses):
	users_words = []
	for user in statuses.keys():
		user_words = {}
		words = []
		for x in statuses[user]:
			x = x.replace('\\n', " ")
			x = x.replace('\\' + 'n', " ")
			for y in x.split():
				y = y.strip(string.punctuation).lower()
				y = y.strip()
				for punc in string.punctuation:
					y = y.replace(punc, "")
				if len(y) > 0:
					words.append(y)
		
		for word in words:
			word = word.strip()
			if word not in user_words:
				user_words[word] = 0
			user_words[word] += 1

		users_words.append({"user_id": user.strip(), 
			"word_counts": user_words})
	# print users_words
	return users_words

def main():
	anew_dict = load_anew_dict()
	anew_words = anew_dict.keys()
	users = {}
	dates = []
	statuses = {}
	status_reader.load_statuses(dates, statuses, users)
	users_words = user_words(statuses)

	userID_color_file = open('userid_hexColor', 'r')
	for line in userID_color_file:
		entry = line.split('\t')
		userid = entry[0].strip()
		color = entry[1].strip()
		for i in xrange(len(users_words)):
			# print users_words[i]["user_id"], userid
			if users_words[i]["user_id"] == userid:
				print userid
				users_words[i]["color"] = color


	total_word_counts = {}
	for user in users_words:
		for word in user["word_counts"]:
			if word not in total_word_counts:
				total_word_counts[word] = 1
			total_word_counts[word] += user["word_counts"][word]

	# Print total word counts
	# for w in sorted(total_word_counts, key=total_word_counts.get, reverse=True):
 #  		print w, total_word_counts[w]

  	# Create Word Count Files
  	for user in users_words:
  		new_file = open("./user_info/" + user["color"] + "_words" , 'w')
  		new_file.write("word" + '\t' + "count" + '\t' + "ANEW" + '\n')
  		for w in sorted(user["word_counts"], key=user["word_counts"].get, reverse=True):
  			if w in anew_words:
	  			new_file.write(w + '\t' + str(user["word_counts"][w]) + '\t' + "1")
	  		else:
	  			new_file.write(w + '\t' + str(user["word_counts"][w]) + '\t' + "0")
  			new_file.write('\n')
  		new_file.close()

	# users_anew_words = {}
	# for user in users_words:
	# 	users_anew_words[user["user_id"]] = []
	# 	user["avg_vl"] = 0.0
	# 	user["avg_ar"] = 0.0
	# 	user["avg_dm"] = 0.0
	# 	for word in user["word_counts"]:
	# 		if word not in total_word_counts:
	# 			total_word_counts[word] = 1b
	# 		total_word_counts[word] += user["word_counts"][word]
	# 		if word in anew_words:
	# 			users_anew_words[user["user_id"]].append(word)
	# 			user["avg_vl"] += float(anew_dict[word][0])
	# 			user["avg_ar"] += float(anew_dict[word][1])
	# 			user["avg_dm"] += float(anew_dict[word][2])


	# for user in users_words:
	# 	print(user["user_id"] + '\t' + \
	# 		str(len(user["word_counts"])) + '\t' + \
	# 		str(len(users_anew_words[user["user_id"]])) + '\t' + \
	# 		str(user["avg_vl"]/len(users_anew_words[user["user_id"]])) + '\t' + \
	# 		str(user["avg_ar"]/len(users_anew_words[user["user_id"]])) + '\t' + \
	# 		str(user["avg_dm"]/len(users_anew_words[user["user_id"]])))
	
if __name__ == "__main__":
    main()
