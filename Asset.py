from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import mplfinance as mpf
from pandas_datareader import data as pdr


class Asset:
    """This class represent a quoted asset (mainly ETFs)
       Entry point of several static analytical methods relative to a stock
    """

    def __init__(self):
        self.ticker = ''
        self.name = ''
        self.isin = ''
        self.id_yahoo = ''
        self.weight = 0.0

    @staticmethod
    def display_Ichimoku(stock: str,
                         date_from: str = '1995-1-1',
                         date_to: str = date.today().strftime("%Y-%m-%d"),
                         horizon: str = '1d') \
            -> None:
        yf.pdr_override()
        data = pd.DataFrame(pdr.get_data_yahoo(stock, start=date_from, end=date_to, interval=horizon, progress=False))
        high9 = data.High.rolling(9).max()
        low9 = data.Low.rolling(9).min()
        high26 = data.High.rolling(26).max()
        low26 = data.Low.rolling(26).min()
        high52 = data.High.rolling(52).max()
        low52 = data.Low.rolling(52).min()

        data['tenkan_sen'] = (high9 + low9) / 2
        data['kijun_sen'] = (high26 + low26) / 2
        data['senkou_A'] = ((data.tenkan_sen + data.kijun_sen) / 2).shift(26)
        data['senkou_B'] = ((high52 + low52) / 2).shift(26)
        data['chikou'] = data.Close.shift(-26)

        data = data.iloc[26:]

        plt.plot(data.index, data['tenkan_sen'], lw=0.8, color='r')
        plt.plot(data.index, data['kijun_sen'], lw=0.8, color='b')
        plt.plot(data.index, data['chikou'], lw=0.8, color='c')
        plt.title('Ichimoku:' + str(stock))
        plt.ylabel("Prices")

        komu = data['Adj Close'].plot(lw=1.3, color='k')
        komu.fill_between(data.index, data.senkou_A, data.senkou_B, where=data.senkou_A >= data.senkou_B,
                          color='lightgreen')
        komu.fill_between(data.index, data.senkou_A, data.senkou_B, where=data.senkou_A < data.senkou_B,
                          color='lightcoral')
        plt.grid()
        plt.show()

    @staticmethod
    def display_volume_candles(stock: str,
                               date_from: str = '1995-1-1',
                               date_to: str = date.today().strftime("%Y-%m-%d"),
                               horizon: str = '1d') \
            -> None:
        yf.pdr_override()
        data = pd.DataFrame(pdr.get_data_yahoo(stock, start=date_from, end=date_to, interval=horizon, progress=False))
        mpf.plot(data, type='candle', title='Price & Volume ' + str(stock), mav=(20), volume=True)

    @staticmethod
    def displayDailyReturnNoiseSingleStock(stock: str, date_from: str = '1995-1-1', date_to: str = date.today()) \
            -> None:
        yf.pdr_override()
        data = pd.DataFrame(pdr.get_data_yahoo(stock, start=date_from, end=date_to, progress=False))
        data[stock] = ((data['Adj Close'] / data['Adj Close'].shift(1)) - 1) * 100
        data[stock].plot(figsize=(8, 5), legend=stock)
        plt.show()

    @staticmethod
    def compute_Arith_return(stock: str, date_from: str, date_to: str) -> float:
        yf.pdr_override()
        data = pd.DataFrame(pdr.get_data_yahoo(stock, start=date_from, end=date_to, progress=False))
        endingValue = data.tail(1)['Adj Close'].iloc[0]
        beginningValue = data.head(1)['Adj Close'].iloc[0]

        return (endingValue / beginningValue - 1) * 100

    @staticmethod
    def compute_Volatility(stock: str, date_from: str, date_to: str) -> float:
        yf.pdr_override()
        data = pd.DataFrame(pdr.get_data_yahoo(stock, start=date_from, end=date_to, progress=False))['Adj Close']
        returns = ((data / data.shift(1)) - 1) * 100
        returns.std()

        return returns.std()
