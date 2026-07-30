import streamlit as st

from src.data_fetcher import get_stock_data, get_stock_info
from src.analysis import add_indicators, calculate_rsi
from src.charts import (
    build_price_chart,
    build_volume_chart,
    build_volatility_chart,
)

st.set_page_config(
    page_title="AlphaSight",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AlphaSight")

ticker = st.text_input("Enter a ticker", value="NVDA")

if ticker:

    # Fetch data
    data = get_stock_data(ticker)
    data = add_indicators(data)
    data["RSI"] = calculate_rsi(data)

    if data.empty:
        st.error("Invalid ticker symbol.")
        st.stop()

    # Fetch company information
    info = get_stock_info(ticker)

    # Risk metrics
    avg_daily_return = data["Daily Return"].mean()
    current_volatility = data["Volatility"].iloc[-1]
    current_rsi = data["RSI"].iloc[-1]

    # Price information
    current_price = info.get("currentPrice", data["Close"].iloc[-1])
    previous_close = info.get("previousClose", data["Close"].iloc[-2])

    change_pct = ((current_price - previous_close) / previous_close) * 100

    st.metric(
        label=ticker.upper(),
        value=f"${current_price:.2f}",
        delta=f"{change_pct:.2f}%"
    )

    # Company metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Market Cap",
        f"${info.get('marketCap', 0) / 1e12:.2f} T"
    )

    col2.metric(
        "P/E Ratio",
        str(info.get("trailingPE", "N/A"))
    )

    col3.metric(
        "Volume",
        f"{info.get('volume', 0) / 1e6:.1f} M"
    )

    col4.metric(
        "52 Week Range",
        f"${info.get('fiftyTwoWeekLow', 0):.2f} - ${info.get('fiftyTwoWeekHigh', 0):.2f}"
    )

    # Risk Metrics
    st.subheader("📊 Risk Metrics")

    risk_col1, risk_col2, risk_col3 = st.columns(3)

    risk_col1.metric(
        "Volatility (Annualized)",
        f"{current_volatility:.1%}"
    )

    risk_col2.metric(
        "Average Daily Return",
        f"{avg_daily_return:.3%}"
    )

    if current_rsi > 70:
        rsi_status = "🔴 Overbought"
    elif current_rsi < 30:
        rsi_status = "🟢 Oversold"
    else:
        rsi_status = "🟡 Neutral"

    risk_col3.metric(
        "RSI (14-day)",
        f"{current_rsi:.1f}"
    )

    risk_col3.caption(rsi_status)

    st.divider()

    # Charts
    show_ma = st.checkbox("Show Moving Averages", value=True)

    st.plotly_chart(
        build_price_chart(
            data,
            ticker.upper(),
            show_ma
        ),
        width="stretch"
    )

    st.plotly_chart(
        build_volume_chart(
            data,
            ticker.upper()
        ),
        width="stretch"
    )

    st.plotly_chart(
        build_volatility_chart(
            data,
            ticker.upper()
        ),
        width="stretch"
    )

    # Raw data
    with st.expander("View Raw Data"):
        st.dataframe(data, width="stretch")