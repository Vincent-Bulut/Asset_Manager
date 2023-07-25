import pandas as pd
import numpy as np
import Tools
from datetime import date
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf
import seaborn as sns
from Asset import Asset


class Portfolio:
    """This class represent all assets managed portfolio"""

    def __init__(self, pfolioName: str, pfolioAum: float) -> None:
        self.name = pfolioName
        self.aum = pfolioAum
        self.assets = dict()
        self.arithmetic_return_a = '0%'
        self.log_return_a = '0%'
        self.volatility_a = '0%'
        self.unsystematicRisk = 0.0
        self.systematicRisk = 0.0

    def computeArithReturn_a(self, date_from: str = '1995-1-1', date_to: str = date.today()) -> None:
        # annualized arithmetic return
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
        self.arithmetic_return_a = Tools.reformatRateWith2D(np.dot(returns_a, weights))

    def computeLogReturn_a(self, date_from: str = '1995-1-1', date_to: str = date.today()) -> None:
        # annualized log return
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
        self.log_return_a = Tools.reformatRateWith2D(np.dot(returns_a, weights))

    def displayAssetEvolutions(self, date_from: str = '1995-1-1', date_to: str = date.today()) -> None:
        data = pd.DataFrame()
        yf.pdr_override()

        for code in self.assets.keys():
            data[code] = pd.DataFrame(pdr.get_data_yahoo(code,
                                                         start=date_from,
                                                         end=date_to,
                                                         progress=False))['Adj Close']

        (data / data.iloc[0] * 100).plot(figsize=(15, 6))
        plt.show()

    def displayAssetRiskReturn_a(self, date_from: str = '1995-1-1', date_to: str = date.today()) -> None:
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
        plt.bar(tickers, returns_a, color='blue', label='Return', alpha=0.5)
        plt.legend(loc="upper right")
        plt.xticks(rotation=90)
        plt.show()

    def displayCorrelationMatrix(self, date_from: str = '1995-1-1', date_to: str = date.today()) -> None:
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

    def computePfolioVolatility_a(self, date_from: str = '1995-1-1', date_to: str = date.today()) -> None:
        # annualized volatility of the portfolio
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
        self.volatility_a = Tools.reformatRateWith2D(np.dot(weights.T, np.dot(returns.cov() * 250, weights)) ** 0.5)

    def computeSystematicRisks(self, date_from: str = '1995-1-1', date_to: str = date.today()) -> None:
        # Diversifiable risk ~ Unsystematic Risk
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

    def getMostCorrelAsset(self, stock: str, date_from: str = '1995-1-1', date_to: str = date.today()) -> list:
        data = pd.DataFrame()
        yf.pdr_override()

        for code in self.assets.keys():
            data[code] = pd.DataFrame(pdr.get_data_yahoo(code,
                                                         start=date_from,
                                                         end=date_to,
                                                         progress=False))['Adj Close']

        returns = ((data / data.shift(1)) - 1) * 100
        corr_matrix = returns.corr()

        dico = {}
        for ind in corr_matrix.index:
            if ind != stock:
                continue

            for c in corr_matrix.columns:
                if c == stock or corr_matrix[c][ind] < 0:
                    continue
                dico[c] = corr_matrix[c][ind]

            if len(dico) == 0:
                return []
            else:
                tmpList = []
                mostCorrelAsset = max(dico, key=dico.get)
                tmpList.append(mostCorrelAsset)
                tmpList.append(dico[mostCorrelAsset])
                mostCorrelAsset = tmpList

                return mostCorrelAsset

    def resumeRiskReturn_IntoXl(self, dateRef: str = date.today().strftime("%Y-%m-%d")) -> None:
        listOfAssetCodes = []
        listOfAssetNames = []

        nbOfPeriod = 9

        returns = []
        volatilities = []

        data = {'Code': [], 'Name': [], 'Period': [], 'From': [], 'To': [], 'Rt': [], 'Vol': []}

        dicoPeriods = Tools.getPeriodsFrom(dateRef)

        for code in self.assets.keys():
            listOfAssetCodes.append(code)
            listOfAssetNames.append(self.assets[code].name)

            listOfAssetCodes += [' - '] * (nbOfPeriod - 1)
            listOfAssetNames += [' - '] * (nbOfPeriod - 1)

            returns.append(round(Asset.compute_Arith_return(code, dicoPeriods['YTD'], dateRef), 2))
            returns.append(round(Asset.compute_Arith_return(code, dicoPeriods['1M'], dateRef), 2))
            returns.append(round(Asset.compute_Arith_return(code, dicoPeriods['3M'], dateRef), 2))
            returns.append(round(Asset.compute_Arith_return(code, dicoPeriods['6M'], dateRef), 2))
            returns.append(round(Asset.compute_Arith_return(code, dicoPeriods['1Y'], dateRef), 2))
            returns.append(round(Asset.compute_Arith_return(code, dicoPeriods['2Y'], dateRef), 2))
            returns.append(round(Asset.compute_Arith_return(code, dicoPeriods['3Y'], dateRef), 2))
            returns.append(round(Asset.compute_Arith_return(code, dicoPeriods['5Y'], dateRef), 2))
            returns.append(round(Asset.compute_Arith_return(code, dicoPeriods['10Y'], dateRef), 2))

            volatilities.append(round(Asset.compute_Volatility(code, dicoPeriods['YTD'], dateRef), 2))
            volatilities.append(round(Asset.compute_Volatility(code, dicoPeriods['1M'], dateRef), 2))
            volatilities.append(round(Asset.compute_Volatility(code, dicoPeriods['3M'], dateRef), 2))
            volatilities.append(round(Asset.compute_Volatility(code, dicoPeriods['6M'], dateRef), 2))
            volatilities.append(round(Asset.compute_Volatility(code, dicoPeriods['1Y'], dateRef), 2))
            volatilities.append(round(Asset.compute_Volatility(code, dicoPeriods['2Y'], dateRef), 2))
            volatilities.append(round(Asset.compute_Volatility(code, dicoPeriods['3Y'], dateRef), 2))
            volatilities.append(round(Asset.compute_Volatility(code, dicoPeriods['5Y'], dateRef), 2))
            volatilities.append(round(Asset.compute_Volatility(code, dicoPeriods['10Y'], dateRef), 2))

            data['Code'] = listOfAssetCodes
            data['Name'] = listOfAssetNames
            data['Period'] += dicoPeriods.keys()
            data['From'] += dicoPeriods.values()
            data['To'] += [dateRef] * nbOfPeriod
            data['Rt'] = returns
            data['Vol'] = volatilities

        df = pd.DataFrame(data, columns=['Code',
                                         'Name',
                                         'Period',
                                         'From',
                                         'To',
                                         'Rt',
                                         'Vol'])

        df.to_excel('perfMon.xlsx')

    def displayAssetAllocationSimulations(self, date_from: str = '1995-1-1', date_to: str = date.today()) -> None:
        """Get a thousand simulations of risk/returns relative to a combination of asset allocations
           Put the result into xl file
        """

        data = pd.DataFrame()
        yf.pdr_override()

        for code in self.assets.keys():
            data[code] = pd.DataFrame(pdr.get_data_yahoo(code,
                                                         start=date_from,
                                                         end=date_to,
                                                         progress=False))['Adj Close']

        log_returns = np.log(data / data.shift(1))
        num_assets = len(pd.unique(log_returns.columns))

        pfolio_returns = []
        pfolio_volatilities = []

        i = 0

        pfolio_id = []
        pfolio_ret_a = []
        pfolio_vol_a = []
        pfolioAssets = []
        weightAssets = []
        weightAssets_std = []

        for x in range(1000):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            weights_std = np.std(weights)
            pfolio_returns.append(np.sum(weights * log_returns.mean()) * 250)
            pfolio_volatilities.append(np.sqrt(np.dot(weights.T, np.dot(log_returns.cov() * 250, weights))))
            pfolio_id.append('P' + str(i))
            pfolio_ret_a.append(pfolio_returns[i])
            pfolio_vol_a.append(pfolio_volatilities[i])
            pfolioAssets.append(' '.join(log_returns.columns))
            weightAssets.append(' '.join(str(weights)))
            weightAssets_std.append(weights_std)
            i += 1

        pfolio_returns = np.array(pfolio_returns)
        pfolio_volatilities = np.array(pfolio_volatilities)

        dic = {'Portfolio': pfolio_id,
               'Returns': pfolio_ret_a,
               'Volatilities': pfolio_vol_a,
               'Assets': pfolioAssets,
               'Weights': weightAssets,
               'Weights_std': weightAssets_std
               }

        df = pd.DataFrame(dic, columns=['Portfolio',
                                        'Returns',
                                        'Volatilities',
                                        'Assets',
                                        'Weights',
                                        'Weights_std'])

        df.to_excel('results.xlsx')

        portfolios = pd.DataFrame({'Return': pfolio_returns, 'volatilities': pfolio_volatilities})
        portfolios.plot(x='volatilities', y='Return', kind='scatter', figsize=(10, 6))

        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Return')
        plt.show()

    def info(self, dt_from: str, dt_to: str = date.today()) -> None:
        products = [x.name for x in self.assets.values()]
        print(f"Managed Portfolio : {self.name}\n")
        print(f"Portfolio Assets period from {dt_from} to {dt_to}")
        for stock, code in zip(products, list(self.assets.keys())):
            print(f"-{stock}")
            print(f"   Arithmetic return: {Tools.reformatRateWith2D(Asset.compute_Arith_return(code,dt_from,dt_to))}")
            print(f"   Volatility from: {Tools.reformatRateWith2D(Asset.compute_Volatility(code,dt_from,dt_to))}")
        self.computeArithReturn_a(dt_from, dt_to)
        self.computePfolioVolatility_a(dt_from, dt_to)
        print(f"\nannualized portfolio return: {self.arithmetic_return_a}")
        print(f"annualized portfolio volatility: {self.volatility_a}")




