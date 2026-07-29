import streamlit as st
from src.data_fetcher import get_stock_data, get_stock_info
from src.charts import build_price_chart, build_volume_chart

st.set_page_config(
    page_title="AlphaSight",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AlphaSight")

ticker = st.text_input("Enter a ticker", value="NVDA")

if ticker:

    data = get_stock_data(ticker)

    if data.empty:
        st.error("Invalid ticker symbol.")
        st.stop()

    info = get_stock_info(ticker)

    current_price = info.get("currentPrice", data["Close"].iloc[-1])
    previous_close = info.get("previousClose", data["Close"].iloc[-2])

    change_pct = ((current_price - previous_close) / previous_close) * 100

    st.metric(
        label=ticker.upper(),
        value=f"${current_price:.2f}",
        delta=f"{change_pct:.2f}%"
    )

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

    st.divider()

    show_ma = st.checkbox("Show Moving Averages", value=True)

    st.plotly_chart(
        build_price_chart(
            data,
            ticker.upper(),
            show_ma
        ),
        use_container_width=True
    )
    st.plotly_chart(
        build_volume_chart(
            data,
            ticker.upper()
        ),
        use_container_width=True
    )

    with st.expander("View Raw Data"):
        st.dataframe(data, use_container_width=True)