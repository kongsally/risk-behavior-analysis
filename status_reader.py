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
# print plotly_id, plotly_api
py.sign_in(plotly_id, plotly_api)


def xldate_to_datetime(xldate):
  tempDate = datetime.datetime(1900, 1, 1)
  deltaDays = datetime.timedelta(days=int(xldate))
  secs = (int((xldate%1)*86400)-60)
  detlaSeconds = datetime.timedelta(seconds=secs)
  TheTime = (tempDate + deltaDays + detlaSeconds )
  return TheTime.strftime("%Y")


def load_statuses(dates, statuses, users):
	with open('training_data.tsv', 'rb') as tsvfile:
		status_reader = tsvfile.read().splitlines()
		for row in status_reader:
			row = row.split('\t')
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
	status_count_file = open(status_file_name + "_count.csv", 'w')
	status_file = open(status_file_name + ".csv", 'w')
	
	for user_id in statuses.keys():
		for stat in statuses[user_id]:
			if any(word in stat.split(" ") for word in keywords):
				if user_id in keyword_stats.keys():
					keyword_stats[user_id].append(stat)
				else:
					keyword_stats[user_id] = [stat]

	for x in keyword_stats.keys():
		status_count_file.write(x + ',\"' + str(len(keyword_stats[x])) + '\"\n')
		for y in keyword_stats[x]:
			status_file.write(x + ',\"' + y + '\"\n')

	with open(status_file_name + '.json', 'w') as outfile:
    		json.dump(keyword_stats, outfile, ensure_ascii=False)


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
	    title='Facebook Users by Status Countss'
	)
	fig = go.Figure(data=data, layout=layout)
	plot_url = py.plot(fig, filename='stat_count_year')

def status_piechart(sex, alcohol, drug, violence) :

	total_stat_count = {}
	for user in sex.keys():
		total_stat_count[user] = [len(sex[user]), 0, 0, 0]

	for user in alcohol.keys():
		if user in total_stat_count.keys():
			total_stat_count[user][1] = len(alcohol[user])
		else:
			total_stat_count[user] = [0, 1, 0, 0]

	for user in drug.keys():
		if user in total_stat_count.keys():
			total_stat_count[user][2] = len(drug[user])
		else:
			total_stat_count[user] = [0, 0, 1, 0]

	for user in violence.keys():
		if user in total_stat_count.keys():
			total_stat_count[user][3] = len(violence[user])
		else:
			total_stat_count[user] = [0, 0, 0, 1]


	total_userIDs = total_stat_count.keys()
	sex_counts = []
	alcohol_counts = []
	drug_counts = []
	violence_counts = []

	for i in range(0, len(total_userIDs)):
		sex_counts.append(total_stat_count[total_userIDs[i]][0])
		alcohol_counts.append(total_stat_count[total_userIDs[i]][1])
		drug_counts.append(total_stat_count[total_userIDs[i]][2])
		violence_counts.append(total_stat_count[total_userIDs[i]][3])

	sex_sum = sum(sex_counts)
	alcohol_sum = sum(alcohol_counts)
	drug_sum = sum(drug_counts)
	violence_sum = sum(violence_counts)

	total_sum = sex_sum + alcohol_sum + drug_sum + violence_sum + 0.0

	fig = {
		"data": [
			{
				"values" : sex_counts,
				"labels" : total_userIDs,
				"name" : "Sex",
				"hole": .5,
     			"type": "pie",
     			"domain": {"x": [0, 0.2]},
     			'textinfo':'none'
			},
			{
				"values" : alcohol_counts,
				"labels" : total_userIDs,
				"name" : "Alcohol",
				"hole": .5,
      			"type": "pie",
      			"domain": {"x": [0.22, 0.42]},
      			'textinfo':'none'
			},
			{
				"values" : drug_counts,
				"labels" : total_userIDs,
				"name" : "Drug",
				"hole": .5,
      			"type": "pie",
      			"domain": {"x": [0.44, 0.64]},
      			'textinfo':'none'
			},
			{
				"values" : violence_counts,
				"labels" : total_userIDs,
				"name" : "Drug",
				"hole": .5,
      			"type": "pie",
      			"domain": {"x": [0.66, 0.86]},
      			'textinfo':'none'
			}

		],
		"layout" : {
			"title": "Number of Facebook Statuses with Sex, Alcohol, Drug, or Violence Content",
			"annotations": [
            {
                "font": {
                    "size": 13
                },
                "showarrow": False,
                "text": "Sex: " + str(sex_sum),
                "x": 0.05,
                "y": 0.15
            },
            {
                "font": {
                    "size": 13
                },
                "showarrow": False,
                "text": "Alcohol: " + str(alcohol_sum),
                "x": 0.27,
                "y": 0.15
            },
            {
                "font": {
                    "size": 13
                },
                "showarrow": False,
                "text": "Drug: " + str(drug_sum),
                "x": 0.54,
                "y": 0.15
            },
            {
                "font": {
                    "size": 13
                },
                "showarrow": False,
                "text": "Violence: " + str(violence_sum),
                "x": 0.81,
                "y": 0.15
            }]

		}
	}

	plot_url = py.plot(fig, filename='status_by_content')




def main():

	users = {}
	dates = []
	statuses = {}
	load_statuses(dates, statuses, users)

	stat_lengths = {}
	for user in statuses.keys():
		stat_lengths[user] = len(statuses[user])

	user_by_freq = sorted(stat_lengths, key=stat_lengths.get, reverse=True)
	for x in user_by_freq:
		print x + '\t' + str(stat_lengths[x])
	print len(user_by_freq)


	sex_statuses = {}
	sex_keywords = []
	with open('sex_keywords.csv', 'r') as f:
		reader = csv.reader(f)
		sex_keywords = list(reader)[0]
	sex_keywords = [x.strip() for x in sex_keywords]
	print_statuses("sex", statuses, sex_keywords, sex_statuses)

	alcohol_statuses = {}
	alcohol_keywords = []
	with open('alcohol_keywords.csv', 'r') as f:
		reader = csv.reader(f)
		alcohol_keywords = list(reader)[0]
	alcohol_keywords = [x.strip() for x in alcohol_keywords]
	print_statuses("alcohol", statuses, alcohol_keywords, alcohol_statuses)

	drug_statuses = {}
	drug_keywords = []
	with open('drug_keywords.csv', 'r') as f:
		reader = csv.reader(f)
		drug_keywords = list(reader)[0]
	drug_keywords = [x.strip() for x in drug_keywords]
	print_statuses("drug", statuses, drug_keywords, drug_statuses)

	violence_statuses = {}
	violence_keywords = []
	with open('violence_keywords.csv', 'r') as f:
		reader = csv.reader(f)
		violence_keywords = list(reader)[0]
	violence_keywords = [x.strip() for x in violence_keywords]
	print_statuses("violence", statuses, violence_keywords, violence_statuses)

	# status_piechart(sex_statuses, alcohol_statuses, drug_statuses, violence_statuses)

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
	# status_bargraph(users.keys(), formatted_dates, user_by_freq, users)


if __name__ == "__main__":
    main()



