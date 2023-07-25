import Tools
import Portfolio as pf
from Asset import Asset as a
from datetime import datetime
from dateutil.relativedelta import relativedelta

dt_ref = '2023-2-2'
stock_ref = 'PANX.PA'
myAssets = Tools.getAllAssetFromXlFile("PEA.xlsx", "holdings")
P = pf.Portfolio('Vincent Portfolio', 70E3)
P.assets = myAssets
P.info(dt_from=dt_ref)
P.displayAssetEvolutions(dt_ref)
P.displayAssetRiskReturn_a(dt_ref)
P.displayCorrelationMatrix(dt_ref)
print(P.getMostCorrelAsset('LGWT.DE', dt_ref))
P.resumeRiskReturn_IntoXl()
P.displayAssetAllocationSimulations(dt_ref)

# Focus NASDDAQ
a.display_Ichimoku(stock_ref, datetime.strptime(dt_ref, "%Y-%m-%d").date() - relativedelta(years=3))
a.display_volume_candles(stock_ref, dt_ref)
a.displayDailyReturnNoiseSingleStock(stock_ref, dt_ref)







