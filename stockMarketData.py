
import pandas as pd
import os
import time 
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators  # will calcualte moving average
import matplotlib.pyplot as plt
import json 
from userClass import Stock 



'''
	Purpose: Get stock market data

	Inputs: 
			Stocks - Object Stocks 
			api_key - alpha_vantage so we can change keys for every different threat 
			api_key - second key so we wont get errors 

	Outputs: Will give the stock a EMA, VWAP & plot it 
			 And will decide when to buy or sell a stock

'''
def getStockData(Stock, api_key, api_key2 ): # for later on we will get the actual stock object
	currentSymbol = Stock.Symbol 

	ts = TimeSeries(key=api_key, output_format = 'pandas')
	ti = TechIndicators(key= api_key2, output_format = 'pandas')


	### WE NEED TO LOOK FOR WHAT STOCKS TO LOOK FOR #######
	## BEFORE ENTERIG THE WHILE LOOP 				#######




	############################## THIS INFINITE LOOP IS WHERE WE GET DAILY DATA ##########################
	run = 1 
	count = 1;

	while run < 3:
		data, meta_data = ts.get_intraday(symbol=currentSymbol, interval = '1min', outputsize = 'compact') 
		dataTI, metaDataTi = ti.get_ema(symbol = currentSymbol, interval = '1min', time_period = 40, series_type = 'open')
		dataVWAP, metaDataTiV = ti.get_vwap(symbol = currentSymbol, interval = '1min')

		differenceVWAP = dataVWAP.size - data['1. open'].size  # this will make the onto the same points 
		differenceEMA = dataTI.size - data['1. open'].size

		df1 = dataTI.iloc[differenceEMA-1::] # illoc will return the index staring at differenceEMA up to the end of the list 
		df2 = data['1. open']
		df3 = dataVWAP.iloc[differenceVWAP- 1::] # will make the VMWAP data as same length as price data


		##### CHECK THAT THE PRICES CORSSES THE EMA LINE && PRICE IS UNDER VWAP ##########  

		t_df1 = df1['EMA'] # this is so I can get a max value 
		t_df3 = df3['VWAP'] 
		lastEMA =	t_df1.max();
		lastPRICE =	df2.max() ;
		lastVWAP = t_df3.max() ;

		print("lastEMA = ", lastEMA)
		print("lastVWAP =  " , lastVWAP ) 
		print("lastPRICE = " , lastPRICE)

		total_df = pd.concat([df1, df2, df3], axis = 1)  # puts both data on one graph
		total_df.plot()
		plt.draw() 
		plt.pause(70) # this will pause the image for  61 seconds 
		#plt.show(block = False) # this will make non-blocking  block=false


		print(count) 
		count = count + 1
		print("hello \n")






