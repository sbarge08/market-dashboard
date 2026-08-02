import streamlit as st
import yfinance as yf

@st.cache_data(ttl=300)
def get_stock_data(ticker_symbol, period="6mo"):
    stock = yf.Ticker(ticker_symbol)
    return stock.history(period=period)


@st.cache_data(ttl=300)
def get_stock_info(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    return stock.info


@st.cache_data(ttl=900)
def get_news(ticker_symbol, max_items=5):
    stock = yf.Ticker(ticker_symbol)

    news_items = stock.news

    articles = []

    for item in news_items[:max_items]:

        content = item.get("content", item)

        articles.append(
            {
                "title": content.get(
                    "title",
                    "Untitled"
                ),
                "publisher": content.get(
                    "provider",
                    {}
                ).get(
                    "displayName",
                    "Unknown source"
                ),
                "link": content.get(
                    "canonicalUrl",
                    {}
                ).get(
                    "url",
                    ""
                ),
            }
        )

    return articles