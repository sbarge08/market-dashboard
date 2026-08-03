import streamlit as st

from src.data_fetcher import (
    get_stock_data,
    get_stock_info,
    get_news,
)
from src.analysis import add_indicators, calculate_rsi
from src.charts import (
    build_price_chart,
    build_volume_chart,
    build_volatility_chart,
)
from src.company import display_company_profile
st.set_page_config(
    page_title="AlphaSight",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
# 📈 AlphaSight

##### Professional Market Intelligence Dashboard
"""
)

st.divider()

st.sidebar.title("AlphaSight")
st.sidebar.subheader("⭐ Watchlist")

watchlist = [
    "NVDA",
    "AAPL",
    "MSFT",
    "AMZN",
    "TSLA",
]
selected_stock = st.sidebar.selectbox(
    "Choose from Watchlist",
    watchlist
)

ticker = st.sidebar.text_input(
    "Or Enter a Ticker",
    value=selected_stock
).strip().upper()
time_period = st.sidebar.selectbox(
    "Time Range",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "max",
    ],
    index=2,
)
if ticker:

    with st.spinner("Fetching market data..."):

        try:
            # Fetch stock data
            data = get_stock_data(
    ticker,
    period=time_period,
)
            data = add_indicators(data)
            data["RSI"] = calculate_rsi(data)

            if data.empty:
                st.error("❌ No data found for this ticker.")
                st.stop()

            # Fetch company information
            info = get_stock_info(ticker)
            
           
        except ValueError:
              st.error("❌ Invalid ticker symbol.")
              st.stop()

        except Exception:
            st.error(
                "❌ Unable to retrieve stock data. Please check the ticker symbol or try again later."
            )
            st.stop()

    # -------------------------
    # Risk Metrics
    # -------------------------

    avg_daily_return = data["Daily Return"].mean()
    current_volatility = data["Volatility"].iloc[-1]
    current_rsi = data["RSI"].iloc[-1]

    # -------------------------
    # Price Information
    # -------------------------

    current_price = info.get(
        "currentPrice",
        data["Close"].iloc[-1]
    )

    previous_close = info.get(
        "previousClose",
        data["Close"].iloc[-2]
    )

    change_pct = (
        (current_price - previous_close)
        / previous_close
    ) * 100
market_trend = "🟢 Bullish"

if change_pct < 0:
    market_trend = "🔴 Bearish"
with st.container(border=True):

    left, right = st.columns([4, 1])

    with left:

        st.markdown(f"# {info.get('longName', ticker)}")

        st.caption(
            f"{ticker} • "
            f"{info.get('sector', 'Unknown Sector')} • "
            f"{info.get('industry', 'Unknown Industry')}"
        )

    with right:

        st.metric(
            "Current Price",
            f"${current_price:.2f}",
            f"{change_pct:.2f}%"
        ) 

  # -------------------------
# Company Metrics
# -------------------------

with st.container(border=True):

    left_col, right_col = st.columns([1, 2])

    with left_col:
        display_company_profile(info)

    with right_col:
     st.subheader("📊 Market Metrics")
     top_row = st.columns(2)
    bottom_row = st.columns(2)
    top_row[0].metric(
        "Market Cap",
        f"${info.get('marketCap', 0) / 1e12:.2f} T"
    )

    top_row[1].metric(
        "P/E Ratio",
        str(info.get("trailingPE", "N/A"))
    )

    bottom_row[0].metric(
        "Volume",
        f"{info.get('volume', 0) / 1e6:.1f} M"
    )

    bottom_row[1].metric(
        "52 Week Range",
        f"${info.get('fiftyTwoWeekLow', 0):.2f} - ${info.get('fiftyTwoWeekHigh', 0):.2f}"
    )
    # -------------------------
    # Risk Metrics Display
    # -------------------------
with st.container(border=True):

    st.subheader("📊 Market Summary")

    summary_col1, summary_col2 = st.columns(2)

    summary_col1.metric(
        "Current Price",
        f"${current_price:.2f}",
        f"{change_pct:.2f}%"
    )

    summary_col2.metric(
        "Trend",
        market_trend
    )

    summary_col3, summary_col4 = st.columns(2)

    summary_col3.metric(
        "RSI",
        f"{current_rsi:.1f}"
    )

    summary_col4.metric(
        "Volatility",
        f"{current_volatility:.1%}"
    )

st.divider()
with st.container(border=True):

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

    # -------------------------
    # Charts
    # -------------------------
with st.container(border=True):
    show_ma = st.checkbox(
        "Show Moving Averages",
        value=True
    )

    st.plotly_chart(
        build_price_chart(
            data,
            ticker,
            show_ma,
        ),
        width="stretch",
    )

    st.plotly_chart(
        build_volume_chart(
            data,
            ticker,
        ),
        width="stretch",
    )

    st.plotly_chart(
        build_volatility_chart(
            data,
            ticker,
        ),
        width="stretch",
    )

    # -------------------------
    # Raw Data
    # -------------------------

    st.subheader("📰 Recent News")

try:
    articles = get_news(ticker)

except Exception:
    articles = []

if not articles:

    st.caption("No recent news available right now.")

else:

   for article in articles:

    st.markdown(
        f"**[{article['title']}]({article['link']})**  \n"
        f"*Source: {article['publisher']}*"
    )