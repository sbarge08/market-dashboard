import yfinance as yf


def get_stock_data(ticker_symbol, period="6mo"):
    stock = yf.Ticker(ticker_symbol)
    history = stock.history(period=period)

    history["Daily Return"] = history["Close"].pct_change()
    history["MA20"] = history["Close"].rolling(20).mean()
    history["MA50"] = history["Close"].rolling(50).mean()

    return history


def get_stock_info(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    return stock.info
