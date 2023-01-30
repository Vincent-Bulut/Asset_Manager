import Tools
import Portfolio as pf
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

date_ref = datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d").date()
date_ref -= relativedelta(years=1)
myAssets = Tools.getAllAssetFromXlFile("PEA.xlsx", "holdings")

P = pf.Portfolio('vince', 122000)
P.assets = myAssets
ll = P.getMostCorrelAsset('GLUX.PA', '2023-01-01')

print(ll)
P.displayAssetEvolutions(date_ref)




