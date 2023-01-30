import pandas as pd
import Asset
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from pandas.tseries.offsets import BDay


def getAllAssetFromXlFile(xlPath, shtName):
    data = pd.read_excel(xlPath, sheet_name=shtName)
    data.columns = data.columns.str.replace(' ', '_')
    dicoAssets = dict()

    for row in data.itertuples():
        anAsset = Asset.Asset()
        anAsset.ticker = getattr(row, 'Bloomberg_Ticker')
        anAsset.name = getattr(row, 'Product_Name')
        anAsset.isin = getattr(row, 'ISIN')
        anAsset.id_yahoo = getattr(row, 'Code')
        anAsset.weight = getattr(row, 'Weight')
        dicoAssets[anAsset.id_yahoo] = anAsset

    return dicoAssets


def reformatRateWith2D(val):
    return str(round(val, 2)) + ' %'


def displayObjectAttributes(obj):
    return list(set(dir(obj)) - set(dir(object)))


def adjustWorkingDayFormat(dateRef : datetime):
    if dateRef.weekday() < 5:
        return dateRef.strftime("%Y-%m-%d")
    else:
        return (dateRef - BDay(1)).strftime("%Y-%m-%d")


def getPeriodsFrom(dateRef):
    dico_periods = {}
    dt_to = datetime.strptime(dateRef, "%Y-%m-%d").date()

    dt_ytd = date(dt_to.year - 1, 12, 31)
    dt_1M = dt_to - relativedelta(months=1)
    dt_3M = dt_to - relativedelta(months=3)
    dt_6M = dt_to - relativedelta(months=6)
    dt_1Y = dt_to - relativedelta(years=1)
    dt_2Y = dt_to - relativedelta(years=2)
    dt_3Y = dt_to - relativedelta(years=3)
    dt_5Y = dt_to - relativedelta(years=5)
    dt_10Y = dt_to - relativedelta(years=10)

    dico_periods['YTD'] = dt_ytd
    dico_periods['1M'] = dt_1M
    dico_periods['3M'] = dt_3M
    dico_periods['6M'] = dt_6M
    dico_periods['1Y'] = dt_1Y
    dico_periods['2Y'] = dt_2Y
    dico_periods['3Y'] = dt_3Y
    dico_periods['5Y'] = dt_5Y
    dico_periods['10Y'] = dt_10Y

    for k, v in dico_periods.items():
        dico_periods[k] = adjustWorkingDayFormat(dico_periods[k])

    return dico_periods


# dtt = '2023-01-29'
# dico = getPeriodsFrom(dtt)
#
# for k, v in dico.items():
#     print(k + ': ' + v)