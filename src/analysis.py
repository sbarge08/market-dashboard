def add_indicators(data):
    data = data.copy()

    data["Daily Return"] = data["Close"].pct_change()

    data["MA20"] = data["Close"].rolling(window=20).mean()

    data["MA50"] = data["Close"].rolling(window=50).mean()

    data["Volatility"] = (
        data["Daily Return"]
        .rolling(window=20)
        .std()
        * (252 ** 0.5)
    )

    return data
def calculate_rsi(data, window=14):
    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi
