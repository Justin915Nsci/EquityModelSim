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
from matplotlib import style
import tkinter as tk
import time
#import schedule
import sched
style.use("fivethirtyeight")        #can use any style available on https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html

def main():
    #win = tk.Tk()
    #win.title("$tonks #money")
    #win.geometry("400x400")
    #title = tk.Label(text="Sup Hustlas, y'all ready to make some $$$?")
    #title.grid(column = 0, row =0)        
    #button1 = tk.Button(text="Rise and Grind", bg = "red")
    #button1.grid(column = 0, row =1)    
    #ef1 = tk.Entry()
    #ef1.grid(column =0, row =2)
    #win.mainloop()
    s = sched.scheduler(time.time,time.sleep)
    print("Welcome to tradez.")
    symb = input("Enter the trade symbol of the stock you want to track:")
    data = getData(symb)
    while(data==False):
        symb = input("Enter the trade symbol of the stock you want to track:")
        data=getData(symb)
    displayData(data)
    while True:
        s.enter(60,1,refresh,(symb,))     #need comma after symb to make it 1 argument instead of #arg = #char
        s.run()
        print("update")
    #data = schedule.every(5).seconds.do(getdata,symb)
    #schedule.every(5).seconds.do(displayData,data)
    
    #while True:
     #   schedule.run_pending()
      #  time.sleep(1)
def refresh(symb):
    data = getData(symb)
    displayData(data)

def getData(symb):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + str(symb) + "&interval=1min&apikey=" + api_key;
    #url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + symb + "&interval=1min&outputsize=full&apikey=" + api_key;    For getting full 1400 data points
    #------------------------------------------------------------------------------------------------------------------------------------------------
    #data = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=BMO&interval=1min&apikey=" + api_key);
    data = requests.get(url);
    if data.status_code == 200:
        #print("(data)bag secured")
        pass
    else:
        print("Data fetching failed")
        return False
    data = data.json()          #get data in json format
    if "Error Message" in data:
        print("I'm sorry that symbol is not regonized")
        return False
    #show data at this key
    #data = data['Meta Data']
    data = data['Time Series (1min)']
    #data = dict(data.items()[:480])  dictionaries are not subscriptable
    
    #print(data)
    return data

def displayData(data):
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
    data['5min'] = np.round(data['close'].rolling(window=5).mean(),2)
    data['30min'] = np.round(data['close'].rolling(window=30).mean(),2)
    #print(data['5min'])
    data['5min'].plot()
    #data['5min'].legend()
    #data['30min'].plot()
    data['close'].plot()
    plt.legend()
    plt.show()
    return True

main()
