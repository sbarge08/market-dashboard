import yfinance as yf


def get_stock_data(ticker_symbol, period="6mo"):
    stock = yf.Ticker(ticker_symbol)
    return stock.history(period=period)


def get_stock_info(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    return stock.info