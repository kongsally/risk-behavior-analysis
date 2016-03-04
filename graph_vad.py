import csv
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import os
import operator

plotly_id = os.environ['PLOTLY_ID']
plotly_api = os.environ['PLOTLY_API_KEY']
# print plotly_id, plotly_api
py.sign_in(plotly_id, plotly_api)


user_ids = []
valence = []
arousal = []
dominance = []

with open('user_anew_word_count', 'rb') as tsvfile:
		status_reader = tsvfile.read().splitlines()
		for row in status_reader:
			row = row.split('\t')
			user_ids.append(row[0])
			valence.append(float(row[3]))
			arousal.append(float(row[4]))
			dominance.append(float(row[5]))


print sum(valence)
print sum(valence) / len(valence)
print sum(arousal)
print sum(arousal) / len(arousal)
print sum(dominance)
print sum(dominance) / len(dominance)

# val_bar = go.Bar(
# 	x = user_ids,
# 	y = valence,
# 	name='Valence Level'
# )

# aro_bar= go.Bar(
# 	x = user_ids,
# 	y = arousal,
# 	name='Arousal Level'
# )

# dom_bar = go.Bar(
# 	x = user_ids,
# 	y = dominance,
# 	name='Dominance Level'
# )

# data = [val_bar, aro_bar, dom_bar]
# layout = go.Layout(
# 	title="Users' Valence Arousal Dominance Level"
# )

# fig = go.Figure(data=data, layout=layout)
# plot_url = py.plot(fig, filename='user_word_vad')

