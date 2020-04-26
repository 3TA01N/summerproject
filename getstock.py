import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from matplotlib.backends.backend_pdf import PdfPages

style.use("ggplot")

start = dt.datetime(1980,1,1)
end = dt.datetime.now()

#fed rate etc
rates = ["UNRATE","FEDFUNDS"]
bond =["DGS30","DGS10","DGS2"]
#stocks
stocks = ["VTI","QQQ","ABBV","T","MO","SPHD"]
stocks2 = ["LMT","BA"]
stocks3 = ["KSS","MCD","KO"]

#fed
fr = web.DataReader(rates,"fred",start,end)
bd = web.DataReader(bond,"fred",start,end)
dt = web.DataReader("GFDEGDQ188S","fred",start,end)
#dividend
dv = web.DataReader(stocks+stocks2+stocks3,"yahoo-actions")
dv2 = web.DataReader(stocks2,"yahoo-actions")
dv3 = web.DataReader(stocks3,"yahoo-actions")

#house
hs = web.DataReader(["SFXRSA","CSUSHPINSA"],"fred",start,end)
#stock price
st = web.DataReader(stocks,"yahoo",start,end)
st2 = web.DataReader(stocks2,"yahoo",start,end)
st3 = web.DataReader(stocks3,"yahoo",start,end)


#plot fed rate
#pdf = PdfPages("eco1.pdf")
gdp = web.DataReader(["GDPC1"],"fred",start,end)
gdp.plot(figsize=(20,2))
plt.savefig("test.png")


# plt.figure()
# hs.plot(figsize=(20,2),title="SF,US House Price index")
# pdf.savefig(hs)

# dt.plot(figsize=(20,2),title="Total Public Debt/GDP")
# fr.plot(figsize=(20,2))
# bd.plot(figsize=(20,2))
# st["Close"].plot(figsize=(20,2))
# st2["Close"].plot(figsize=(20,2))
# st3["Close"].plot(figsize=(20,2))

# #plot stock yield
# for stock in dv.keys():
    # plt.figure()
    # dv[stock]["value"].plot(label=stock,figsize=(20,3),title=stock)
    # pdf.savefig(plt)