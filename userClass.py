import pandas as pd 
import matplotlib.pyplot as plt 


'''
User Object will have atributes 

	cash - amount of not used money

	Stock - Will give atributes to object Stock
			-Symbol
			-price
			-EMA 
			-VWAP
			-amount 
			-profit 
			
	Profit (Amount of gain money)

	Aggressive Mode 
		1. OPTIMAL - Price have to be cross EMA line and will use VWAP f
		2. AGRESIVE - Will buy every time it price crosses EMA line 

'''
class Stock: 
	Time = [] # for the time that the stocks are being accessed 

	# the only thing we initialize it with the Symbol
	def __init__(self, Symbol):
		self.Symbol = Symbol
		self.CurrentPrice = 0
		self.Amount = 0
		self.InitialPrice = 0 
		self.EMA = [] 
		self.VWAP = []
		self.Price = []
		self.Own = 0;


	def setEMA (self, emaVal): ## we should be passing a list 
		self.EMA = emaVal 

	def setVWAP (self, vwapVal):
		self.VWAP = vwapVal

	def buy(self):
		self.Own = 1

	def sell(self):
		self.Own = 0

	def setCurrentAmount(self, amount):
		self.Amount = amount 

	def addToAmount ( self, addAmount):
		self.Amount = self.Amount + addAmount
		print ("Current Amount is  ", self.Amount)
		return self.Amount

	def currentStockProfit(self, currentPrice ):
		self.CurrentStockProfit = (currentPrice - self.InitialPrice)*self.Amount 
		print ("The current Profit is ", self.CurrentStockProfit)
		return self.CurrentStockProfit

	def addTime(self, time):
		self.Time.append(time)

	def setPrice(self, price):
		self.Price.append(price)
		self.CurrentPrice = price

	def setDataFrame(self):
		# GETTING EMA SAME SIZE AS TIME AND PRICE 
		#differenceEMA = len(self.EMA) - len(self.Time) 
		## I still need to get ride of the elements at the beginning that are not being used 
		data = {'Price' : self.Price}  # , 	'EMA':self.EMA, 	'VWAP':self.VWAP }	
		
		self.df = pd.DataFrame(data,index = self.Time )

	def printGraph(self ): # this will plot the graph 
		self.df.plot()
		plt.draw()
		plt.pause(70)# will leave it plot for 40 seconds







class User:
	NumOfTrades = 0
	AgresitivyMode = 1  # optimal mode 
	numOfStocks = 0
	#numOfWatching = 0

	# Default constructor 
	def __init__(self, Cash, CurrentProfit): # note Stocks is a array of stocks 
		self.Cash = Cash
		self.CurrentProfit = CurrentProfit
		self.Stocks = [] 			# list of own stocks 
		self.WatchingStocks = [] 	# list of watching stocks 

	def setStocks ( self,  Stocks ):
		self.Stocks = Stocks 

	def addOneStock( stock ):
		self.Stocks.append(stock)
		numOfStocks = numOfStocks + 1

	def setWatchList ( self, WatchingStocks ):
		self.WatchingStocks = WatchingStocks

	def addOne2watchList(self, Stock ):
		self.WatchingStocks.append(Stock ) 
		#numOfWatching = numOfWatching + 1

	'''
	IS BETTER TO GET THE CURRENT PROFIT FROM ROBINHOOD 
	def currentTotalProfit():
		for i in self.Stocks 
			i.currentPrice(c_getCurrentPrice ) # c_getCurrentPrice will get the price of currentStock
	'''


	def setCurrentProfit (self, CurrentPRofit):
		self.CurrentProfit = CurrentPRofit 
		print ("The Current Profit is  " , self.CurrentProfit)

	def setCash(self, Cash):
		self.Cash = Cash










