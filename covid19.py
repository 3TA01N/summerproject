import numpy as np
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO
import base64
from flask import Flask, render_template, request, current_app, g
from flask.cli import with_appcontext
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine


#create object to access database(cursor)
#open connection at beginning, keep open until user exits

app = Flask(__name__)

socketio = SocketIO(app)
Bootstrap(app)


#sqlite database
engine = create_engine('sqlite:///coviddata.db', echo=True)
sqlite_connection = engine.connect()
# def get_db():
	# if 'db' not in g:
		# g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
	# return g.db

# def close_db(e=None):
	# db = g.pop('db', None)
	# if db is not None:
		# db.close()
		


#@socketio.on('deathes checked', namespace='/test')
#def dChecked(message):


#covid variables
cases = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
deathes = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")


country = cases.groupby('Country/Region')
countryDeathes = deathes.groupby('Country/Region')
 
Sweden = country.get_group(name='Sweden')
SwedenTotal = (Sweden.sum(axis = 0)).drop(labels = ['Country/Region', 'Lat', 'Long', 'Province/State'])

UnitedStates = country.get_group(name='US')
UnitedStatesTotal = (UnitedStates.sum(axis = 0)).drop(labels = ['Country/Region', 'Lat', 'Long', 'Province/State'])

Italy = country.get_group(name='Italy')
ItalyTotal = (Italy.sum(axis = 0)).drop(labels = ['Country/Region', 'Lat', 'Long', 'Province/State'])

ChinaCases = country.get_group(name='China')
ChinaDeathes = (((countryDeathes.get_group(name='China')).sum(axis = 0)).drop(labels = ['Country/Region', 'Lat', 'Long', 'Province/State'])).tolist()
ChinaTotal = ((ChinaCases.sum(axis = 0)).drop(labels = ['Country/Region', 'Lat', 'Long', 'Province/State'])).to_frame()
ChinaTotal['Deathes'] = ChinaDeathes
ChinaTotal = ChinaTotal.reset_index()
ChinaTotal.columns = ['Dates', 'Cases', 'Deathes']

WorldTotal = (cases.sum(axis = 0)).drop(labels = ['Country/Region', 'Lat', 'Long'])

#stock
Start = dt.datetime(2020,1,1)
End = dt.datetime.now()
def convdate(datevalue):
	return datevalue.strftime("%#m/%#d/%y")
dji = web.DataReader(['^DJI'], data_source='yahoo', start=Start,end=End)
dji = dji['Volume']
print(dji.columns)

dji = dji.reset_index()	
dji.columns = ['Dates', 'dji value']
dji['Dates'] = dji['Dates'].map(lambda a: convdate(a))
dji['Dates'] = dji['Dates'].astype(str)
dji.plot(x = 'Dates', y = 'dji value', figsize=(20,2))

#merge
print(dji)
print(ChinaTotal)
print(pd.merge(dji, ChinaTotal, on='Dates'))


#WORKING SO FAR
sqlite_table = "chinadb"
ChinaTotal.to_sql(sqlite_table, sqlite_connection, if_exists='append')
#engine.execute('SELECT * FROM test').fetchall()
print(chinadb.fetchall())

def plot():
	total = eval(str(request.url_rule)[1:] + "Total")
	print(total)
	if request.method == 'POST':
		print(request.form.getlist('checkbox1'))
		if 'deathes' in request.form.getlist('checkbox1') and 'cases' in request.form.getlist('checkbox1'):
			total.plot()
		elif 'cases' in request.form.getlist('checkbox1'):
			print("CASES")
			total.plot(x='Dates', y='Cases')
		elif 'deathes' in request.form.getlist('checkbox1'):
			print("DEATHES")
			total.plot(x='Dates', y='Deathes')




    



# @app.route("/hello")
# def home():
	# return render_template('index.html')

@app.route("/China", methods=['GET', 'POST'])
def graphpage():
	print(ChinaTotal)
	plot()
	imgfile = BytesIO()
	plt.savefig(imgfile, format='png')
	imgfile.seek(0)
	imgdata_png = imgfile.getvalue()
	imgdata_png = base64.b64encode(imgdata_png).decode('ascii')
	return render_template('page1.html', picture=imgdata_png)
	
	
if __name__ == "__main__":	
	socketio.run(app, debug=True)
	# app.run(debug=True)
		

