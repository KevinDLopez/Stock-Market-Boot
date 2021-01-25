
import stockMarketData		# This is making a reference of all the functions ( so I can access the global variables )
import userClass
import browserControl
import threading 

from stockMarketData import * # this is making copies of all the functions ( so we don't need to specify where each function comes form )
from userClass import *
from userClass import * 
from browserControl import * 




# we will get what stocks to look for on from other programs 
##  THIS PROGRAM WILL ONLY GET DATA FROM ALPHA_VATAGE
s1 = Stock('NVDA')

api_key_list = ['39F0L5GTVJVI0RON', 'MBW2BAPIPJK2AFO8', '3GQNAGCCXNIF1EN8' ] 
api_key_list.append ('564QXVKJ03XAFO4X')
api_key_list.append('OGOGRK2B73MJQRFF')
api_key_list.append('5SIWA2DDI2ZPTICC') # size 6 
api_key_list.append('WG45CM41VEMPVVFQ')
api_key_list.append('NQF2CJSFMROOK1FH')# size 8 

print(api_key_list)

threadList = []


##########################################################################################
###################################### MAIN FUCNTION #####################################
##########################################################################################
def main():
	print("python main function")
	signInAndGetData()
	threadCounter = 0

	for indi_stock in browserControl.Kevin.WatchingStocks:	# we need to specify where the list come from
		#print( indi_stock.Symbol ) # Print the stocks symbol
		# instead of printing were gonna try to get data using alpha_vantage
		t = threading.Thread( target = getStockData, name = 'thread{}'.format(indi_stock.Symbol), args = (indi_stock, api_key_list[threadCounter], api_key_list[threadCounter]) ) # this will create a threat that will execute The getting data form alpha_vantage
		threadList.append(t) # add threads to a list 

		#getStockData(indi_stock, api_key, api_key2)t
	#note threadList = the nuber of stocks 
	#we cnat execute htat number of threads at the same time 
	# so we need to create something that will share it at the same time 
	threadCounter = 0
	for i in threadList: # it will only look at the frist 5 stocks 
		if threadCounter < 5 :
			i.start() # start 4 threads 
			threadCounter += 1 
		else:
			# do nothing 
			print("we already have 4 threads started") 
			break # break out of the for loop 




##########################################################################################
###################################### MAIN FUCNTION #####################################
##########################################################################################



if __name__ == '__main__':
	main()
	print('i')


