import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from flask import Flask
from io import BytesIO
import base64
from flask import render_template

cases = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

countries = cases.groupby('Country/Region')
countrylist = cases["Country/Region"].unique()
Sweden = countries.get_group(name='Sweden')
US = countries.get_group(name='US')
Italy = countries.get_group(name='Italy')
China = countries.get_group(name='China')
ChinaTotal = (China.sum(axis = 0)).drop(labels = ['Country/Region', 'Lat', 'Long', 'Province/State'])
USTotal = (US.sum(axis = 0)).drop(labels = ['Country/Region', 'Lat', 'Long', 'Province/State'])
SwedenTotal = (Sweden.sum(axis = 0)).drop(labels = ['Country/Region', 'Lat', 'Long', 'Province/State'])
ItalyTotal = (Italy.sum(axis = 0)).drop(labels = ['Country/Region', 'Lat', 'Long', 'Province/State'])
WorldTotal = (cases.sum(axis = 0)).drop(labels = ['Country/Region', 'Lat', 'Long'])

def plotData():
	ChinaTotal.plot(label="China")
	USTotal.plot(label="US")
	SwedenTotal.plot(label="Sweden")
	ItalyTotal.plot(label="Italy")
	WorldTotal.plot(label="World")
	ax = plt.subplot(111)
	plt.legend(loc="upper left")
	plt.xticks(rotation=90)


app = Flask(__name__)
@app.route("/hello")

def HelloWorld():
	plotData()
	imgfile = BytesIO()
	plt.savefig(imgfile, format='png')
	imgfile.seek(0)
	imgdata_png = imgfile.getvalue()
	imgdata_png = base64.b64encode(imgdata_png).decode('ascii')
	return render_template('index.html', picture=imgdata_png)
	
	
if __name__ == "__main__":
	app.run(debug=True)
		
