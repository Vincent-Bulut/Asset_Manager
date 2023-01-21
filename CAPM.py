
import pandas as pd
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf


def display_pFolio_CAPM(tickers, date_from='1995-1-1', date_to=date.today()):
    myData = pd.DataFrame()

    yf.pdr_override()
    for t in tickers:
        myData[t] = pd.DataFrame(pdr.get_data_yahoo(t, start=date_from, end=date_to, progress=False))['Adj Close']

    log_returns = np.log(myData / myData.shift(1))
    print(log_returns)
    num_assets = len(tickers)

    pfolio_returns = []
    pfolio_volatilities = []

    for x in range(1000):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        pfolio_returns.append(np.sum(weights * log_returns.mean()) * 250)
        pfolio_volatilities.append(np.sqrt(np.dot(weights.T, np.dot(log_returns.cov() * 250, weights))))

    pfolio_returns = np.array(pfolio_returns)
    pfolio_volatilities = np.array(pfolio_volatilities)

    portfolios = pd.DataFrame({'Return': pfolio_returns, 'volatilities': pfolio_volatilities})
    portfolios.plot(x='volatilities', y='Return', kind='scatter', figsize=(10, 6))
    plt.scatter(0.24, 3.439, color='red')

    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.show()


tickers = ['LVMH.MI', 'RNO.PA']
display_pFolio_CAPM(tickers, '2023-1-1')