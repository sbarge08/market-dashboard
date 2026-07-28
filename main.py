import yfinance as yf


def get_stock_data(ticker_symbol, days="6mo"):
    stock = yf.Ticker(ticker_symbol)
    history = stock.history(period=days)

    history["Ticker"] = ticker_symbol
    history["Daily Return"] = history["Close"].pct_change()

    return history


nvda_data = get_stock_data("NVDA")

print(nvda_data[["Close", "Daily Return"]].head(10).to_string())
average_daily_return = nvda_data["Daily Return"].mean()

print(
    f"\nAverage daily return: {average_daily_return:.4%}"
)