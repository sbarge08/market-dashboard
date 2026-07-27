import yfinance as yf

nvda = yf.Ticker("NVDA")

data = nvda.history(period="5d")

print(data)