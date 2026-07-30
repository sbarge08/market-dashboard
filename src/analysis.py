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