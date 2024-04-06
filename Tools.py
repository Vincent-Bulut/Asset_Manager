import pandas as pd
import Asset as a
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from pandas.tseries.offsets import BDay


def getAllAssetFromXlFile(xlPath: str, sheetName: str) -> dict:
    """Get Assets'features from Excel source
       Headers: Bloomberg Ticker|Product Name|ISIN|Code|Weight
    """

    data = pd.read_excel(xlPath, sheet_name=sheetName)
    data.columns = data.columns.str.replace(' ', '_')
    dicoAssets = dict()

    for row in data.itertuples():
        anAsset = a.Asset()
        anAsset.ticker = getattr(row, 'Bloomberg_Ticker')
        anAsset.name = getattr(row, 'Product_Name')
        anAsset.isin = getattr(row, 'ISIN')
        anAsset.id_yahoo = getattr(row, 'Code')
        anAsset.weight = getattr(row, 'Weight')
        dicoAssets[anAsset.id_yahoo] = anAsset

    return dicoAssets


def getPeriodsFrom(dateRef: str) -> dict:
    """Get the exact date from a reference date relative to a period"""

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


def reformatRateWith2D(val: float) -> str:
    return str(round(val, 2)) + ' %'


def adjustWorkingDayFormat(dateRef: datetime) -> str:
    if dateRef.weekday() < 5:
        return dateRef.strftime("%Y-%m-%d")
    else:

def calcul_impot(revenu_net_imposable):
    tranches = [
        (0, 10777, 0),
        (10778, 27478, 0.11),
        (27479, 79533, 0.30),
        (79534, 164935, 0.41),
        (164936, float('inf'), 0.45)
    ]
    
    impot = 0
    for borne_inf, borne_sup, taux in tranches:
        if revenu_net_imposable > borne_inf:
            impot += min(revenu_net_imposable, borne_sup) - borne_inf * taux
        else:
            break
            
    return impot

# Exemple d'utilisation
# revenu_net_imposable = 30000  # Mettez votre revenu net imposable ici
# impot_a_payer = calcul_impot(revenu_net_imposable)
# print(f"L'impôt à payer est de {impot_a_payer}€")
        return (dateRef - BDay(1)).strftime("%Y-%m-%d")



