import sys
import platform
import time
import inspect

####  note i can probably use interups so that I can help the program while in run time
###   there is a libary called signal that does has the interups in pythno
import requests

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from userClass import User
from userClass import Stock
from alpha_vantage.techindicators import TechIndicators
import threading

import multiprocessing

from multiprocessing import Manager 


############## TABS ##########################
# TAB 1		=		GETTIGN PRICES
# ANY TOHER TAB WILL BE TO BUY OR SELL STOCKS
# WINDOWS


api_key_list = ['39F0L5GTVJVI0RON', 'MBW2BAPIPJK2AFO8', '3GQNAGCCXNIF1EN8']
api_key_list.append('564QXVKJ03XAFO4X')
api_key_list.append('OGOGRK2B73MJQRFF')
api_key_list.append('5SIWA2DDI2ZPTICC')  # size 6
api_key_list.append('WG45CM41VEMPVVFQ')
api_key_list.append('NQF2CJSFMROOK1FH')  # size 8

'''####################################################################
Purpose: 	This function will open robin hood  

Inputs :	None

Outputs:	Store on user.list the stocks we have and store its amount 

'''  ####################################################################
browserLock = threading.Lock()  # This will make thread wait while is locked ( only be locked while using selenium driver on )
priceLock = threading.Lock()  # This will be locked when we are updating and getting prices of stocks


def signInAndGetData():
    global Kevin
    global browser  # like this were going to be able to access the browser form outside this function
    global robinhood
    global youtube
    global options

    print(platform.system())

    if (platform.system() == "Windows"):
        print("Its a windows")
        options = Options()
        options.add_argument(
            "user-data-dir=C:\\Users\\kevin\\AppData\\Local\\Google\\Chrome\\User Data")  # C:\Users\kevin\AppData\Local\Google\Chrome\User Data\Default")
    elif (platform.system() == "Darwin"):
        print("Its a mac")  # /Users/Kevin/Library/Application Support/Google/Chrome/Profile 1
        options = Options()
        options.add_argument("user-data-dir=/Users/Kevin/Library/Application Support/Google/Chrome")  # C:\Users\kevin\AppData\Local\Google\Chrome\User Data\Default")

    robinhood = "https://robinhood.com"
    youtube = "https://www.youtube.com/"

    browser = webdriver.Chrome(chrome_options=options)  # this will open my own profile
    # browser.send_keys(goToPriceTabW)
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL, '1')

    browser.get(robinhood)

    # it ifs my mac wait longer
    if (platform.system() == "Windows"):
        time.sleep(3)
    elif (platform.system() == "Darwin"):
        time.sleep(15)
    # getting the money
    moneyStr = browser.find_element_by_class_name('QzVHcLdwl2CEuEMpTUFaj').text  # this will return a string
    print(moneyStr)
    # sb = moneyStr[1: len(moneyStr)]  # this will create a subString with out the first character '$'
    # remove any commas
    moneyOnlyNum = []  # make it a list first because it doesnt let us append to strings
    for i in moneyStr:
        if '0' <= i <= '9' or i == '.':
            moneyOnlyNum.append(i)
            # print(i)
      #
    moneyStr = ''.join(moneyOnlyNum)
    print("gettign money")
    print(moneyStr)

    tempMoney = float(moneyStr)  # convert  string to integer
    Kevin = User(tempMoney, 0)

    print("Kevins Cash ", Kevin.Cash)  # this should print what we are reading as money

    elementsStocksList = browser.find_elements_by_class_name('_3HLJ3tNpwWnaSGO61Xz-VA')  # this is an array of elements

    print("You have ", len(elementsStocksList), " Stocks")

    for i in elementsStocksList:
        Kevin.addOne2watchList(Stock(i.text))  # Kevin is getting the stocks filled

    print("SignInAndGetData is done \n")


'''####################################################################
	Purpose: Get Stock market data from robin-hood

	inputs 

	Outputs: Will get an array with the prices of the stock
'''  ####################################################################

def getStockPrices():
    prices = []  # array of prices
    percentages = []
    run5 = 0
    pricesAndPercenteges = []
    while run5 >= 0: # infinitive loop
        browserLock.acquire()
        try:
            print("The lock for browser was just given to getStockPrices")
            browser.get("https://www.google.com/")  # open another browser so we can clear up the catch form selenium
            time.sleep(1)
            browser.find_element_by_id('hplogo')

            browser.get(robinhood)  # refresh the page every single time we get new data

            if (platform.system() == "Windows"):
                time.sleep(3)
            elif (platform.system() == "Darwin"):
                time.sleep(8)

            # run5 += 1 # so it will run 5 times

            ##########################  NOTE THIS IS WHERE IM NOT GETTING AN UPDATED ELEMENT ########################
            if run5 % 2 == 0:
                pricesAndPercenteges = browser.find_elements_by_class_name('_3nOWC25YX1zvfGc0inK1iE')  # this will give us 154 elements
            else:
                pricesAndPercenteges = browser.find_elements_by_class_name('_2jxaLrMhW0qe-ghIvDBXx4')

        finally:
            browserLock.release()
        print("The lock for brwoser was just release from getStockPrices") 

        #print(len(pricesAndPercenteges))
        count = 0
        for i in pricesAndPercenteges:
            if (count % 2 == 0):  # this will be a one is odd
                # First element will be price
                # This function will get here first
                tempS = i.text
                print("TempS = ")
                print(tempS) 
                numS = tempS[1: len(tempS)]  # get ride of the first character '$'
                prices.append(float(numS))  # FLOATS
            else:  # is going to be the percentage value
                percentages.append(i.text)  # strings

            count = count + 1

        #########for loop

        count = 0

        priceLock.acquire()
        try:
            print("The lock for price was just given to getStockPrices")
            for i in Kevin.WatchingStocks:
                i.setPrice(prices[count])  # add current prcice to its relative stocks
                count += 1
                #print(i.Symbol, " ", i.CurrentPrice)
            ###### for loop
            #print("the size of the prices is = " + str(len(i.Price)))
            t = time.localtime()
            current_time = time.strftime("%H%M%S", t)
            # current_timeInt =

            Kevin.WatchingStocks[0].addTime(int(current_time))  # it doesnt matter to what stock
        finally:
            priceLock.release()
        print("the lock for price was jsut release out of getStockPrices") 

        # Stock.addTime( int(time.localtime() ))
        time.sleep(1)  # get data every 5 seconds
        pricesAndPercenteges = []
        run5 += 1
        print(run5)


        print("\n this shold be printed every 2 seconds ")

        # end of while run5


    # we need to get data form alpha vantage and put into each stock
    # or we could create our own VWAP or EMA graphs


'''####################################################################
	Purpose: Will decide when to buy stock  

	inputs : 	lastPrice
				lastVWAP
				lastEMA


	Outputs: Will get symbol and will make desition on when to buy stock 
'''  ####################################################################


def lookAtStock(currentVWAP, currentEMA, Stock):
    # check current is under vwap
    # check that previous prices are above EMA
    # check that the current price is crossing the EMA line or could be slightly on top

    currentPrice = Stock.Price[len(Stock.Price) - 1]  # current price
    previousPrice = Stock.Price[len(Stock.Price) - 2]  # previous price

    previousEMA = Stock.EMA[len(Stock.EMA) - 2]
    previousVWAP = Stock.VWAP[len(Stock.VWAP) - 2]

    if currentPrice >= currentEMA and previousPrice <= previousEMA and currentPrice < currentVWAP and Stock.Own == 0:  # at this point the price has crossed the price stock
        # buyStock
        buyStock(Stock)

    if currentPrice <= currentEMA and previousPrice >= previousEMA and Stock.Own == 1:  # Cross EMA line again = Sell stock
        sellStock(Stock)



'''####################################################################
	Purpose: Prints graph using a new process    

	inputs : 	Stock - will print the graph 
				
	Outputs: Graph using matplotlib 
'''  ####################################################################
def printGraphUsingProcess(time, price, VWAP, EMA ):
	#Im gonna need to pass the actual data and do the plotting here///
	# is gonna be array for the time,price, VWAP, and EMA

	Stock.printGraph() 








'''####################################################################
	Purpose: Get Stock VWAP and EMA from alpha_vantage 

	inputs : 
				Stock = Stock Object
				api_key = key for alpha vantage 

	Outputs: Will run for ever
			 & will  make decision on when to buy 
'''  ####################################################################

def getVWAPnEMA(Stock, api_key, api_key2):
    currentSymbol = Stock.Symbol

    # ts = TimeSeries(key=api_key, output_format = 'pandas')
    ti = TechIndicators(key=api_key2, output_format='pandas')
    ti2 = TechIndicators(key=api_key, output_format='pandas')

    ### WE NEED TO LOOK FOR WHAT STOCKS TO LOOK FOR #######
    ## BEFORE ENTERIG THE WHILE LOOP 				#######

    ############################## THIS INFINITE LOOP IS WHERE WE GET DAILY DATA ##########################
    run = 1
    count = 1

    # This will run for ever
    while run < 3:
        # data, meta_data = ts.get_intraday(symbol=currentSymbol, interval = '1min', outputsize = 'compact')
        dataTI, metaDataTi = ti.get_ema(symbol=currentSymbol, interval='1min', time_period=40, series_type='open')
        dataVWAP, metaDataTiV = ti2.get_vwap(symbol=currentSymbol, interval='1min')

        priceLock.acquire()
        try:
            print("the lock for price was just given to getVWAPnEMA")
            differenceVWAP = dataVWAP.size - len(Stock.Price)  # to make the price and VWAP same size
            differenceEMA = dataTI.size - len(Stock.Price)  # make

            df1 = dataTI.iloc[
                  differenceEMA - 1::]  # illoc will return the index staring at differenceEMA up to the end of the list
            df3 = dataVWAP.iloc[differenceVWAP - 1::]  # will make the VMWAP data as same length as price data

            ##### CHECK THAT THE PRICES CORSSES THE EMA LINE && PRICE IS UNDER VWAP ##########
            
            t_df1 = df1['EMA']
            t_df3 = df3['VWAP']

            Stock.setVWAP(t_df3)
            Stock.setEMA(t_df1)

            currentVWAP = t_df1.max();
            currentEMA = t_df3.max();
            lookAtStock(currentVWAP, currentEMA, Stock)  # check if is at a good point to buy
        finally:
            priceLock.release()
        print("the lock for price was just  release out of getVWAPnEMA ") 
        #  print(Kevin.WatchingStocks[0].Price)
        Stock.setDataFrame()  # this will set the pandas data frame

        #  I need to send the data instead of the object 
        		# For now using a manager is the fastest way
        mgr = Manager()
        ns = mgr.Namespace()
        ns.df = Stock

        p = multiprocessing.Process(target = printGraphUsingProcess, args=(ns,))   
        p.start()
        p.join() 

        time.sleep(65)

       #Stock.printGraph()  # print each graph  gaph is not releasing



'''####################################################################
	Purpose: Will control the browser to buy a specific stock 

	inputs : 
				Stock = Stock Object to buy

	Outputs: None
'''  ####################################################################


def buyStock(stock):
    browserLock.acquire()
    try:
        print("The lock for the browser was just given to buyStock")
        browser.get(robinhood)  # I should create a new chrome drive for this

        # will need to control browser driver using
        # price_lock = threading.Lock()

        time.sleep(2)
        xpath = "//*[contains(text(), '"
        xpath += stock.Symbol
        xpath += "')]"
        print(xpath)
        time.sleep(2)
        stockToClick = browser.find_element_by_xpath(xpath).click()

        # ActionChains(browser) .key_down(Keys.CONTROL) .click(stockToClick) \
        #    .key_up(Keys.CONTROL)  .perform()

        time.sleep(2)
        browser.find_element_by_name("quantity").send_keys("000")
        browser.find_element_by_class_name('_1uaripz9PIQ8yApSTs6BKk').click()
    finally:
        browserLock.release()
        print("the browser lock was jsut release out of buyStock")

'''####################################################################
	Purpose: Will control browser to sell a specific stock 

	inputs : z
				Stock = Stock Object to sell 

	Outputs: None
'''  ####################################################################


def sellStock(stock):
    browserLock.aquire()
    try:
        print("The lock for browser was just given to sell stock")
        # I still gotta add code for this
        print("Selling ", stock.Symbol)
        browser.get(robinhood)
        time.sleep(2)
        xpath = "//*[contains(text(), '"
        xpath += stock.Symbol
        xpath += "')]"
        print(xpath)
        browser.find_element_by_xpath(xpath).click()
        time.sleep(2)
        ################### 	THIS LOGIC IS GOING TO BE DIFFERENT ##############
        # browser.find_element_by_name("quantity").send_keys("000")
        # browser.find_element_by_class_name('_1uaripz9PIQ8yApSTs6BKk').click()
        browser.get(robinhood)
    finally:
        browserLock.release()
    print("the lock for browser was just release form sellStock") 


'''####################################################################
	Purpose: Will start 10 threads to track stocks

	inputs : 


	Outputs: 
'''  ####################################################################
def trackTopTen():  # this funtion will track the five stocks on kevins watchlist
    # signInAndGetData()

    ##### CREATE A THREAD THAT WILL TRACK FOR THIS
    # getStockPrices()
    gettingPricesThread = threading.Thread(target=getStockPrices, name='getStockPrices_Thread', args=())
    gettingPricesThread.start()

    time.sleep(20)  # wait for 2 minutes
    print("the 20 seconds are over ")

    ######  CREATE EACH USING TREADS INDIVIDUAL TREADS
    threadVWAPnEMA = []
    for i in range(2):
        # getVWAPnEMA(Kevin.WatchingStocks[i] , api_key_list[i], api_key[i] )
        t = threading.Thread(target=getVWAPnEMA, name='thread{}'.format(Kevin.WatchingStocks[i].Symbol),
                             args=(Kevin.WatchingStocks[i], api_key_list[i], api_key_list[i]))
        # Kevin.WatchingStocks[i].setDataFrame() # this will the list into pandas
        # Kevin.WatchingStocks[i].printGraph() # print each graph
        t.start()
        threadVWAPnEMA.append(t)
        time.sleep(1)

    print("we have 11 threads running at once ")
    print(Kevin.WatchingStocks[0].Price)


##################################################################
##				TESTING
##################################################################
signInAndGetData()

trackTopTen()

print("main thread is done")
while 1:
    time.sleep(7)
    print(Kevin.WatchingStocks[0].Price)

# s =  Stock("DIA")
# buyStock(s)


# trackTopTen()
