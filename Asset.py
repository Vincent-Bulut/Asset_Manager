from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr


class Asset:
    """This class represent a financial asset like stocks, bonds, etc"""

    def __init__(self):
        self.ticker = ''
        self.name = ''
        self.isin = ''
        self.id_yahoo = ''
        self.weight = 0

    @staticmethod
    def displayDailyReturnNoiseSingleStock(stock, date_from='1995-1-1', date_to=date.today()):
        yf.pdr_override()
        data = pd.DataFrame(pdr.get_data_yahoo(stock, start=date_from, end=date_to, progress=False))
        data[stock] = ((data['Adj Close'] / data['Adj Close'].shift(1)) - 1) * 100
        data[stock].plot(figsize=(8, 5), legend=stock)
        plt.show()

    @staticmethod
    def compute_Arith_return(stock, date_from, date_to):
        yf.pdr_override()
        data = pd.DataFrame(pdr.get_data_yahoo(stock, start=date_from, end=date_to, progress=False))
        endingValue = data.tail(1)['Adj Close'].iloc[0]
        beginningValue = data.head(1)['Adj Close'].iloc[0]

        return (endingValue / beginningValue - 1) * 100

    @staticmethod
    def compute_Volatility(stock, date_from, date_to):
        yf.pdr_override()
        data = pd.DataFrame(pdr.get_data_yahoo(stock, start=date_from, end=date_to, progress=False))['Adj Close']
        returns = ((data / data.shift(1)) - 1) * 100
        returns.std()

        return returns.std()




