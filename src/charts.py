import plotly.graph_objects as go


def build_price_chart(data, ticker_symbol, show_ma=True):

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name=ticker_symbol,
        )
    )

    if show_ma:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["MA20"],
                mode="lines",
                name="20-Day MA",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["MA50"],
                mode="lines",
                name="50-Day MA",
            )
        )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_rangeslider_visible=False,
    )

    return fig


def build_volume_chart(data, ticker_symbol):

    colors = [
        "#5FA377"
        if close >= open_
        else "#C06955"
        for open_, close in zip(data["Open"], data["Close"])
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=data.index,
                y=data["Volume"],
                marker_color=colors,
            )
        ]
    )

    fig.update_layout(
        title=f"{ticker_symbol} Volume",
        template="plotly_dark",
        height=220,
    )

    return fig
