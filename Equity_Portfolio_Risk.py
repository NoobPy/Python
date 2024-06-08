import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timedelta as delta
from math import sqrt
from scipy.special import ndtri

ticker = []
while len(ticker) < 10:
    a = input(f'Enter ticker or q to finish')
    if a != 'q':
        ticker.append(a)
    else:
        break

df1 = pd.DataFrame(yf.download(tickers=ticker,end=dt.date(dt.now()),start=dt.date(dt.now()) - delta(days=365*5))['Close'])
daily_ret = df1.apply(lambda x : x/x.shift(1)-1).dropna()
weights = np.array([1/len(ticker) for i in ticker])
market_data  = pd.DataFrame(yf.download(tickers='^GSPC',end=dt.date(dt.now()),start=dt.date(dt.now())-delta(days=365*5))['Close'])
market_ret = market_data.apply(lambda x : x/x.shift(1)-1).dropna()
rf = pd.DataFrame(yf.download(tickers='^FVX',end=dt.date(dt.now()),start=dt.date(dt.now())-delta(days=1))['Close'],columns=['Close'])
daily_portfoio_ret_Series = pd.DataFrame(data=daily_ret.mean(axis=1),columns=['Close'])

#lets implment portfolio std dev
def std_dev(daily_ret):
    cov_mat = daily_ret.cov()
    port_var = np.dot(weights.T,np.dot(cov_mat,weights))
    return sqrt(port_var)

portfolio_std_dev= std_dev(daily_ret)

def ret(daily_ret):
    return daily_ret.mean().mean()

daily_portfolio_ret = ret(daily_ret)


def beta(daily_ret):
    return daily_portfoio_ret_Series['Close'].cov(market_ret['Close'])/np.var(market_ret['Close'])

portfolio_beta = beta(daily_ret)


def sharpe():
    return (daily_portfolio_ret * 252 * 100 - rf.loc[:,'Close'])/(portfolio_std_dev*100*sqrt(252))

portfolio_sharpe = sharpe()

def treynor():
    return (daily_portfolio_ret * 252 * 100 - rf.loc[:,'Close'])/(portfolio_beta)

portfolio_treynor = treynor()


def para_Var():
    return daily_portfolio_ret- ndtri(0.99)*portfolio_std_dev

parametric_var = para_Var()

def Hvar():
    return np.percentile(daily_portfoio_ret_Series,q=1)

historica_var = Hvar()

def perf_plot():
    df_merged = daily_portfoio_ret_Series.merge(market_ret,how='left',left_on='Date',right_on='Date').rename(columns={'Close_x':'Portfolio','Close_y':'SP500'})
    #plt.figure()
    plt.plot(df_merged['Portfolio'],color = 'Green',label = 'Portfolio')
    plt.plot(df_merged['SP500'],color = 'Blue',label = 'SP500')
    plt.title('Portfolio vs SP500')
    plt.xlabel('Time')
    plt.ylabel('Return(%)')
    plt.grid(True)
    plt.legend()
    return plt.show()

print(f'Average daily Equally weighted portfolio return is {round(daily_portfolio_ret*100,2)}%')
print(f'Daily Portfolio volatility is {round(portfolio_std_dev*100,2)}%')
print(f'Portfolio Beta is {round(portfolio_beta,2)}')
print(f'Portfolio Sharpe Ratio is {round(portfolio_sharpe.iloc[-1],2)}')
print(f'Portfolio Treynor Ratio is {round(portfolio_treynor.iloc[-1],2)}')
print(f'Parametric 1 Day 99% Portfoio VaR is {round(parametric_var*100,2)}%')
print(f'Historical 1 Day 99% Portfoio VaR is {round(historica_var*100,2)}%')
perf_plot()


