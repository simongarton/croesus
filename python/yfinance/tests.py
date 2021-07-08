from os import symlink
import yfinance as yf
import numpy as np
import datetime
# ticker = yf.Ticker("FNZ.NZ")

# print(ticker)
# print(ticker.info)
symbol = "AFI.AX"

ticker = yf.Ticker(symbol)

# print(ticker)
#print(ticker.info)
print("{} : {} ({})".format(symbol, ticker.info['regularMarketPrice'], ticker))

data = yf.download("AFI.AX", period="2d",
        group_by='ticker', actions=False)
# aapl=data["AAPL"]
print(data)
afi=data # data["AFI.AX"]

#print(aapl)
print(afi)
print("")
print(afi.index)
print("")
print(afi.keys())
key = np.datetime64('2021-07-08')
print(key)
print(afi.loc[key])
print(afi.loc[key]['Close'])
#print(afi.dtypes)
#print(afi._get_value(datetime.datetime.strptime("2021-07-08", '%Y-%m-%d').date(),'Close'))