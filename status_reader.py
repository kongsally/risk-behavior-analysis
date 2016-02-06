import csv
import xlrd
import datetime
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import os

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
  return TheTime.strftime("%Y-%m")

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

def status_bargraph(x, y, formatted_dates, user_ids, users):
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


def main():

	statuses = {}
	users = {}
	dates = []

	################### SEX ##########################
	sex_file = open('sex_related_statuses', 'w')
	sex_statuses = {}
	with open('./data/statuses.csv', 'rb') as csvfile:
		status_reader = csv.reader(csvfile.read().splitlines())
		for row in status_reader:
			formatted_date = xldate_to_datetime(float(row[4]))
			
			if formatted_date not in dates:
				dates.append(formatted_date)

			if row[1] in users.keys():
				users[row[1]].append(formatted_date)
			else:
				users[row[1]] = [formatted_date]

			if "sex " in row[3] or "naked " in row[3] or "pussy" in row[3]:
				if row[1] in sex_statuses.keys():
					sex_statuses[row[1]].append(row[3])
				else:
					sex_statuses[row[1]] = [row[3]]
				
	for x in sex_statuses.keys():
		print x + '\t' + str(len(sex_statuses[x]))
		for y in sex_statuses[x]:
			sex_file.write(x + '\t' + y + '\n')


	user_ids = []
	for x in users.keys():
		user_ids.append(x)
		
	formatted_dates = sorted(dates)
	z = []

	for x in xrange(len(formatted_dates)):
		z.append([])

	for y in xrange(len(formatted_dates)):
		for x in xrange(len(user_ids)):	
			z[y].append(users[user_ids[x]].count(formatted_dates[y]))

	x = users.keys()
	y = formatted_dates

	status_heatmap(x, y, z)
	y = users.keys()
	x = formatted_dates
	# status_bargraph(x, y, formatted_dates, user_ids, users)


if __name__ == "__main__":
    main()



