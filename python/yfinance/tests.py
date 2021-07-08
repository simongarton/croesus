import yfinance as yf

# ticker = yf.Ticker("FNZ.NZ")

# print(ticker)
# print(ticker.info)

ticker = yf.Ticker("VTS.AX")

# print(ticker)
print(ticker.info)
print(ticker.info['regularMarketPrice'])
