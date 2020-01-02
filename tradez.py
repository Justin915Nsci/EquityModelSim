# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 14:07:37 2019

@author: justi
"""

#https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&apikey=demo(sample)
import requests
api_key = open("alpha.txt",'r').read() #place api key on local file for security.
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np


data = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=BMO&interval=1min&apikey=" + api_key);
if data.status_code == 200:
    print("(data)bag secured")
data = data.json()          #get data in json format
#show data after this string
#data = data['Meta Data']
data = data['Time Series (1min)']
#print(data)
df = pd.DataFrame(columns = ['date','open','high','low','close','volume'])

#d is data, p is price
for d,p in data.items():
        date = dt.datetime.strptime(d,'%Y-%m-%d %H:%M:%S')
        data_row = [date,float(p['1. open']),float(p['2. high']),float(p['3. low']),float(p['4. close']),int(p['5. volume'])]
        df.loc[-1,:] = data_row
        df.index = df.index +1          #for increasing which index of the df to print on
data = df.sort_values('date')
#print(df)
data['close']=data['close'].astype(float)
data['5min'] = np.round(data['close'].rolling(window=5, min_periods = 1).mean(),2)
#print(data['5min'])
data['5min'].plot()
plt.show()

