import yfinance as yf


def get_stock_data(ticker_symbol, days="5d"):
    stock = yf.Ticker(ticker_symbol)
    history = stock.history(period=days)
    history["Ticker"] = ticker_symbol
    return history


# NVIDIA
nvda_data = get_stock_data("NVDA")
print("NVDA")
print(nvda_data)

# Apple
aapl_data = get_stock_data("AAPL")
print("\nAAPL")
print(aapl_data)

# Microsoft
msft_data = get_stock_data("MSFT", days="1mo")
print("\nMSFT")
print(msft_data)


watchlist = ["NVDA", "AAPL", "MSFT"]

print("\nLatest Closing Prices")

for ticker in watchlist:
    result = get_stock_data(ticker, days="5d")

    if result.empty:
        print(f"{ticker}: No data available")
        continue

    latest_close = result["Close"].iloc[-1]
    print(f"{ticker}: ${latest_close:.2f}")