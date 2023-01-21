import pandas as pd
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf
import Utils
import seaborn as sns


class Portfolio:
    """This class represent all assets managed portfolio"""

    def __init__(self, pfolioName, pfolioAum):
        self.name = pfolioName
        self.aum = pfolioAum
        self.assets = dict()
        self.arithmetic_return_a = '0%'
        self.log_return_a = '0%'
        self.volatility_a = '0%'
        self.unsystematicRisk = 0
        self.systematicRisk = 0

    def computeArithReturn_a(self, date_from='1995-1-1', date_to=date.today()):
        data = pd.DataFrame()
        weights = []
        yf.pdr_override()

        for code in self.assets.keys():
            data[code] = pd.DataFrame(pdr.get_data_yahoo(code,
                                                         start=date_from,
                                                         end=date_to,
                                                         progress=False))['Adj Close']
            weights.append(self.assets[code].weight)

        returns = ((data / data.shift(1)) - 1) * 100
        returns_a = returns.mean() * 250
        self.arithmetic_return_a = Utils.reformatRateWith2D(np.dot(returns_a, weights))

    def computeLogReturn_a(self, date_from='1995-1-1', date_to=date.today()):
        data = pd.DataFrame()
        weights = []
        yf.pdr_override()

        for code in self.assets.keys():
            data[code] = pd.DataFrame(pdr.get_data_yahoo(code,
                                                         start=date_from,
                                                         end=date_to,
                                                         progress=False))['Adj Close']
            weights.append(self.assets[code].weight)

        returns = np.log(data / data.shift(1)) * 100
        returns_a = returns.mean() * 250
        self.log_return_a = Utils.reformatRateWith2D(np.dot(returns_a, weights))

    def displayAssetEvolutions(self, date_from='1995-1-1', date_to=date.today()):
        data = pd.DataFrame()
        yf.pdr_override()

        for code in self.assets.keys():
            data[code] = pd.DataFrame(pdr.get_data_yahoo(code,
                                                         start=date_from,
                                                         end=date_to,
                                                         progress=False))['Adj Close']

        (data / data.iloc[0] * 100).plot(figsize=(15, 6))
        plt.show()

    def displayAssetRiskReturn_a(self, date_from='1995-1-1', date_to=date.today()):
        data = pd.DataFrame()
        tickers = []
        yf.pdr_override()

        for code in self.assets.keys():
            data[code] = pd.DataFrame(pdr.get_data_yahoo(code,
                                                         start=date_from,
                                                         end=date_to,
                                                         progress=False))['Adj Close']
            tickers.append(code)

        returns = ((data / data.shift(1)) - 1) * 100
        returns_a = (returns.mean() * 250)
        vol_a = returns.std() * 250 ** 0.5

        plt.figure(figsize=(7, 8))

        plt.subplot(111)
        plt.bar(tickers, vol_a, color='red', label='Volatility')
        plt.bar(tickers, returns_a, color='blue', label='Return')
        plt.legend(loc="upper right")
        plt.xticks(rotation=90)
        plt.show()

    def displayCorrelationMatrix(self, date_from='1995-1-1', date_to=date.today()):
        data = pd.DataFrame()
        yf.pdr_override()

        for code in self.assets.keys():
            data[code] = pd.DataFrame(pdr.get_data_yahoo(code,
                                                         start=date_from,
                                                         end=date_to,
                                                         progress=False))['Adj Close']

        returns = ((data / data.shift(1)) - 1) * 100
        corr_matrix = returns.corr()
        sns.heatmap(corr_matrix, cmap="Greens")
        plt.show()

    def computePfolioVolatility_a(self, date_from='1995-1-1', date_to=date.today()):
        data = pd.DataFrame()
        weights = []
        yf.pdr_override()

        for code in self.assets.keys():
            data[code] = pd.DataFrame(pdr.get_data_yahoo(code,
                                                         start=date_from,
                                                         end=date_to,
                                                         progress=False))['Adj Close']
            weights.append(self.assets[code].weight)

        weights = np.array(weights)
        returns = ((data / data.shift(1)) - 1) * 100
        self.volatility_a = Utils.reformatRateWith2D(np.dot(weights.T, np.dot(returns.cov() * 250, weights)) ** 0.5)

    # Diversifiable risk ~ Unsystematic Risk
    def computeSystematicRisks(self, date_from='1995-1-1', date_to=date.today()):
        data = pd.DataFrame()
        weights = []
        tickers = []
        yf.pdr_override()

        for code in self.assets.keys():
            data[code] = pd.DataFrame(pdr.get_data_yahoo(code,
                                                         start=date_from,
                                                         end=date_to,
                                                         progress=False))['Adj Close']
            weights.append(self.assets[code].weight)
            tickers.append(code)

        weights = np.array(weights)
        returns = ((data / data.shift(1)) - 1) * 100
        pFolio_var = np.dot(weights.T, np.dot(returns.cov() * 250, weights))
        dr = pFolio_var
        for t in tickers:
            ticker_var_a = returns[t].var() * 250
            dr -= ticker_var_a

        self.unsystematicRisk = dr
        self.systematicRisk = pFolio_var - dr
