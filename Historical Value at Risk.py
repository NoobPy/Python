import yfinance as yf
import datetime as dt
import pandas as pd
import numpy as np
import math

ticker = ['AAPL','GOOG','META','MSFT']

#will give the close prices
data = yf.download(ticker, start='2021-04-27',end='2024-04-26')['Close']

#we will get the daily returns in a seperate dataframe
return_data = pd.DataFrame()

#shift(1) means the previous row data
#shift(n) will mean go n rows back and get the data
#we get daily returns on all 4 stocks for last 3 years


return_data['AAPL_D%'] =  data['AAPL']/data['AAPL'].shift(1)-1
return_data['GOOG_D%'] =  data['GOOG']/data['GOOG'].shift(1)-1
return_data['META_D%'] =  data['META']/data['META'].shift(1)-1
return_data['MSFT_D%'] =  data['MSFT']/data['MSFT'].shift(1)-1

return_data['portfolio_D%'] = (return_data['AAPL_D%']+return_data['GOOG_D%']+return_data['META_D%']+return_data['MSFT_D%'])/4

historical_var_95 = np.percentile(return_data['portfolio_D%'].dropna(),q=5)*100

historical_var_975 = np.percentile(return_data['portfolio_D%'].dropna(),q=2.5)*100


historical_var_99 = np.percentile(return_data['portfolio_D%'].dropna(),q=1)*100
