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
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
import tkinter as tk
import time
import sched
import threading
style.use("fivethirtyeight")        #can use any style available on https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
ex = ""

class App(tk.Tk):
    def __init__(self):
            tk.Tk.__init__(self)
            self.title("$tonk Money")
            self.geometry("700x400")
            self.intro = tk.Label(text="Welcome to tradez, UofT's premier application for tracking stocks")
            self.intro.grid(column=0,row=0)
            self.descrip = tk.Label(text = "In the text box below, write the symbol of the stock you want to track. Then when you're ready, hit the button to begin.")
            self.descrip.grid(column=0,row=1)
            self.entry = tk.Entry(self)
            self.entry.grid(column = 0, row =2)
            self.button = tk.Button(text="Rise and Grind", bg = "red", command = self.start)
            self.button.grid(column = 0, row =3)

    def start(self):
        symb = self.entry.get()
        #label_2 = tk.Label(text = str(symb))
        #label_2.grid(column = 0, row =4)
        self.matPlotCanvas(symb)
        self.after(10000,lambda: self.update(symb,1))
        #threading.Thread(target = self.update(symb,)).start()
   
        
    def matPlotCanvas(self,symb):
        #f = tk.Frame(self)
        data = getData(symb)
        data = processData(data)
        
        fig = Figure(figsize=(6,5),dpi=100)
        a = fig.add_subplot(111,xlabel = "Time",ylabel = "Price")
        a.set_xticklabels([])
        
        #data['5min'].plot()
        #data['close'].plot()
        #a.plot(data['15min'], label = "15min SMA")
        a.plot(data['30min'], label = "30min SMA")
        a.plot(data['90min'], label = "90min SMA")
        #a.plot(data['5min'])
        a.plot(data['close'], label = "close")
        fig.legend(loc = "lower left")
    
        fig.set_label("price")
        canvas = FigureCanvasTkAgg(fig,master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(column =0, row = 4)
        fig.tight_layout()
        #tk.Frame.pack(f)
    
  
    def update(self,symb,i):
        self.matPlotCanvas(symb)
        self.say = tk.Label(text = ("Times updated:" + str(i)))
        self.say.grid(column = 0, row =5)
        self.after(10000,lambda: self.update(symb,i+1))
            
            
    
def main():
    app = App()
    
    app.mainloop()
    
    
    #tradez()


def tradez():
    #print("program begins with " + str(threading.active_count()) + "active threads")
    beginThreads = threading.active_count()
    s = sched.scheduler(time.time,time.sleep)
    #ex = ""
    print("Welcome to tradez.")
    symb = input("Enter the trade symbol of the stock you want to track:")
    data = getData(symb)
    while(data==False):
        symb = input("Enter the trade symbol of the stock you want to track:")
        data=getData(symb)
    data = processData(data)
    displayData(data)
    while (ex!="exit"):
        if(threading.active_count()==beginThreads):
            threading.Thread(target = endTask).start()
        #print("ex is " + str(ex))
        if(ex == "exit"):
            break
        else:
            s.enter(60,1,refresh,(symb,))     #need comma after symb to make it 1 argument instead of #arg = #char
            s.run()
        
        #ex = input("Type exit to stop tracking:");

def endTask():
    global ex 
    ex = input("Type 'exit' to stop tracking:")
    if ex == "exit":
        print("Exiting application, process may take up to 60 seconds. Cya later hustla.")
    return False
    
    
def refresh(symb):
    global ex
    if ex != "exit":
        data = getData(symb)
        data = processData(data)
        #print(str(data))
    if ex != "exit":
        displayData(data)
        print("update")

def getData(symb):
    #url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + str(symb) + "&interval=1min&apikey=" + api_key;
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + symb + "&interval=1min&outputsize=full&apikey=" + api_key;    #For getting full 1400 data points
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

def processData(data):
    df = pd.DataFrame(columns = ['date','open','high','low','close','volume'])
    #d is data, p is price
    for d,p in data.items():
        date = dt.datetime.strptime(d,'%Y-%m-%d %H:%M:%S')
        data_row = [date,float(p['1. open']),float(p['2. high']),float(p['3. low']),float(p['4. close']),int(p['5. volume'])]
        df.loc[-1,:] = data_row
        df.index = df.index +1          #for increasing which index of the df to print on
    data = df.sort_values('date')
    data = data.truncate(before = len(df.index)-500);
    #print(type(data));
    #print(df)
    data['close']=data['close'].astype(float)
    #data['5min'] = np.round(data['close'].rolling(window=5).mean(),2)
    #data['15min'] = np.round(data['close'].rolling(window=15).mean(),2)
    
    data['30min'] = np.round(data['close'].rolling(window=30).mean(),2)
    data['90min'] = np.round(data['close'].rolling(window=90).mean(),2)
    
    #print("data processed")
    return data

def displayData(data):
    data['5min'].plot()
    data['close'].plot()
    plt.legend()
    plt.show()
    return True

main()
#tradez()
