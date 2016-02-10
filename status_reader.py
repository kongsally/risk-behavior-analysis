import csv
import xlrd
import datetime
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import os
import json

plotly_id = os.environ['PLOTLY_ID']
plotly_api = os.environ['PLOTLY_API_KEY']
print plotly_id, plotly_api
py.sign_in(plotly_id, plotly_api)

def xldate_to_datetime(xldate):
  tempDate = datetime.datetime(1900, 1, 1)
  deltaDays = datetime.timedelta(days=int(xldate))
  secs = (int((xldate%1)*86400)-60)
  detlaSeconds = datetime.timedelta(seconds=secs)
  TheTime = (tempDate + deltaDays + detlaSeconds )
  return TheTime.strftime("%Y")

def status_heatmap(x, y, z):
	data = [
	    go.Heatmap(
	    	x=x,
	    	y=y,
	        z=z
	        )
	]
	layout = go.Layout(
	   title='Count of Facebook Statuses Over Years'
	)
	fig = go.Figure(data=data, layout=layout)
	plot_url = py.plot(fig, filename='user_stat_heatmap')

def status_bargraph(y, formatted_dates, user_ids, users):
	data = []
	for i in xrange(len(formatted_dates)):
		y_vals = []
		for z in xrange(len(user_ids)):
			y_vals.append(users[user_ids[z]].count(formatted_dates[i]))
		current_trace = go.Bar(
			x = user_ids,
			y = y_vals,
			name = formatted_dates[i]
			)
		data.append(current_trace)

	layout = go.Layout(
	    barmode='stack',
	    title='Count of Facebook Statuses Over Years'
	)
	fig = go.Figure(data=data, layout=layout)
	plot_url = py.plot(fig, filename='stat_count_year')

def load_statuses(dates, statuses, users):
	with open('data/statuses.csv', 'rb') as csvfile:
		status_reader = csv.reader(csvfile.read().splitlines())
		for row in status_reader:
			formatted_date = xldate_to_datetime(float(row[4]))
			
			if formatted_date not in dates:
				dates.append(formatted_date)

			if row[1] in users.keys():
				users[row[1]].append(formatted_date)
			else:
				users[row[1]] = [formatted_date]

			if row[1] in statuses.keys():
				statuses[row[1]].append(row[3])
			else:
				statuses[row[1]] = [row[3]]


def print_statuses(status_file_name, statuses, keywords, keyword_stats):
	status_count_file = open(status_file_name + "_count", 'w')
	status_file = open(status_file_name, 'w')

	for user_id in statuses.keys():
		for stat in statuses[user_id]:
			if any(word in stat.split(" ") for word in keywords):
				if user_id in keyword_stats.keys():
					keyword_stats[user_id].append(stat)
				else:
					keyword_stats[user_id] = [stat]

	for x in keyword_stats.keys():
		status_count_file.write(x + '\t' + str(len(keyword_stats[x])) + '\n')
		for y in keyword_stats[x]:
			status_file.write(x + '\t' + y + '\n')

	with open(status_file_name + '.json', 'w') as outfile:
    		json.dump(keyword_stats, outfile, ensure_ascii=False)


def main():

	users = {}
	dates = []
	statuses = {}
	load_statuses(dates, statuses, users)

	stat_lengths = {}
	for user in statuses.keys():
		stat_lengths[user] = len(statuses[user])
		
	user_by_freq = sorted(stat_lengths, key=stat_lengths.get, reverse=True)
	

	# sex_statuses = {}
	# sex_keywords=["sex", "pussy", "naked", "penis", "rape"]
	# print_statuses("sexual_statuses", statuses, sex_keywords, sex_statuses)

	# alcohol_statuses = {}
	# alcohol_keywords=["drunk", "beer", "rum", "vodka", "tequila"]
	# print_statuses("alcohol_statuses", statuses, alcohol_keywords, alcohol_statuses)

	# drug_statuses = {}
	# drug_keywords=["marijuana", "weed", "cocaine", "crackhead", "smoke"]
	# print_statuses("drug_statuses", statuses, drug_keywords, drug_statuses)

	formatted_dates = sorted(dates)
	z = []

	for x in xrange(len(formatted_dates)):
		z.append([])

	for y in xrange(len(formatted_dates)):
		for x in xrange(len(user_by_freq)):	
			z[y].append(users[user_by_freq[x]].count(formatted_dates[y]))


	#for heatmap
	# status_heatmap(users.keys(), formatted_dates, z)

	#for stacked bargraph
	#status_bargraph(users.keys(), formatted_dates, user_by_freq, users)


if __name__ == "__main__":
    main()



