#lets do Varience - Covarienc Var for equally weighted portfolio of Mega Tech stocks Meta,AAPL,GOOG,NVDIA

#We will take 3year data and calculate 1 day Var at 95,97.5 and 99 confidence interval var


import yfinance as yf
import datetime as dt
import pandas as pd
import numpy as np
import math
from scipy.special import ndtri

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

#the now calculate the daily average portfolio return as mean of daily mean returns of all 4 stocks
avg_portfolio_retun = (return_data['AAPL_D%'].mean()+return_data['GOOG_D%'].mean()+return_data['META_D%'].mean()+return_data['MSFT_D%'].mean())/4

#since this a delta - normal  var we assume that returns of all 4 stocks are normally distributed
#under the mean-var approch of portfolio optimisation we also take a look at how 2 stocks move together
#this is given by covariance. i high +ve covariance means stocks move together in same direction and portfolio becomes more risky
#high -ve covariance means stocks move in different direction and thus we get portfolio diversification benefit
# cov() func will run on the return_data dataframe and give us covariance matrix

cov_matrix = return_data.cov()

#we are assuming equally weighted portfolio
weights = np.array([0.25,0.25,0.25,0.25])

#portfolio variance is given by Σ (w_i^2 * σ_i^2) + Σ Σ (w_i * w_j * σ_ij)
#w_i and w_j are weights of the 2 stocks currenty under consideration
#σ_ij is the covariance of stock i and j
#this is done my matrix multiplication using numpy.dot() func
#Σ (w_i^2 * σ_i^2) represent the contribution of stock i's  variance to portfolio variance
#cov_matrix is (4,4)
#weight is (4,) so np.dot(cov_matrix,weight) will be a (4,) matrix accoutning for Σ Σ (w_i * w_j * σ_ij)
#We now multiple this my transpose of weight to account for variance Σ (w_i^2 * σ_i^2)

portfolio_variance = np.dot(weights.T,np.dot(cov_matrix,weights))

portfolio_sd = math.sqrt(portfolio_variance)

#delta normal var is calculated as Portfolio Return - Zscore * portfolio std deviantion
#ndtri() will give us the zcore for given confidence level

var_95 = (avg_portfolio_retun - ndtri(0.95)*portfolio_sd)*100
var_975 = (avg_portfolio_retun - ndtri(0.975)*portfolio_sd)*100
var_99 = (avg_portfolio_retun - ndtri(0.99)*portfolio_sd)*100






