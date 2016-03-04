import random

userID_file = open('training_userID', 'r')

def random_hexcolor():
	color_chars = [str(i) for i in xrange(0, 10)]
	for i in "ABCDEF":
		color_chars.append(i)
	color = "#"
	for i in xrange(0, 6):
		color += random.choice(color_chars)
	return color

for line in userID_file:
	print line.strip() + '\t' + random_hexcolor()