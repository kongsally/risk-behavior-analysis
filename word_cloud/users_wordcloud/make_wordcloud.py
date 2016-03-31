#!/usr/bin/env python2
"""
Minimal Example
===============
Generating a square wordcloud from FB Statuses.
"""

from os import path
from wordcloud import WordCloud
import status_reader
import sys


d = path.dirname(__file__)

category_ids = open(sys.argv[1]).readlines()
category = category_ids[0]
user_ids = [x.strip()[0:40] for x in category_ids[1:]]

users = {}
dates = []
statuses = {}
status_reader.load_statuses(dates, statuses, users)

category_text = []
for user_id in statuses: 
	user_id_trimmed = user_id[0:40]
	if user_id_trimmed in user_ids:
		for status in statuses[user_id]:
			category_text.append(status)

text_compilation = ' '.join(category_text)

# Generate a word cloud image
wordcloud = WordCloud('../DINOT.otf').generate(text_compilation)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud)
plt.axis("off")


sys.stderr.write("Making Image" + '\n')

# take relative word frequencies into account, lower max_font_size
wordcloud = WordCloud(max_font_size=100, width = 2000, height = 2000,
max_words = 500,relative_scaling=.3, background_color='black').generate(text_compilation)
# plt.figure()
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()

# The pil way (if you don't have matplotlib)
image = wordcloud.to_image()
image.save('Image_' + sys.argv[1],'png')

sys.stderr.write("Done Saving Image " + sys.argv[1] + '\n')