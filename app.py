"""
Live Crypto Market Dashboard
-----------------------------
Pulls real-time cryptocurrency price data from the free CoinGecko public API
(no API key required) and displays it in an auto-refreshing Streamlit dashboard.

Author: <YOUR NAME>
"""

import time
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# App config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Live Crypto Dashboard",
    page_icon="📈",
    layout="wide",
)

COINGECKO_MARKETS_URL = "https://api.coingecko.com/api/v3/coins/markets"
COINGECKO_CHART_URL = "https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

DEFAULT_COINS = ["bitcoin", "ethereum", "solana", "dogecoin", "cardano", "ripple"]


# ---------------------------------------------------------------------------
# Data fetching (cached for a short window so we don't hammer the free API)
# ---------------------------------------------------------------------------
@st.cache_data(ttl=60)
def fetch_market_data(coin_ids: list[str], vs_currency: str = "usd") -> pd.DataFrame:
    """Fetch current market snapshot for a list of coins."""
    params = {
        "vs_currency": vs_currency,
        "ids": ",".join(coin_ids),
        "order": "market_cap_desc",
        "price_change_percentage": "1h,24h,7d",
    }
    response = requests.get(COINGECKO_MARKETS_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data)[
        [
            "id",
            "symbol",
            "name",
            "current_price",
            "market_cap",
            "total_volume",
            "price_change_percentage_1h_in_currency",
            "price_change_percentage_24h_in_currency",
            "price_change_percentage_7d_in_currency",
        ]
    ]
    df.columns = [
        "id",
        "symbol",
        "name",
        "price_usd",
        "market_cap",
        "volume_24h",
        "change_1h_%",
        "change_24h_%",
        "change_7d_%",
    ]
    return df


@st.cache_data(ttl=60)
def fetch_price_history(coin_id: str, days: int = 7) -> pd.DataFrame:
    """Fetch historical price series for a single coin (for the trend chart)."""
    url = COINGECKO_CHART_URL.format(coin_id=coin_id)
    params = {"vs_currency": "usd", "days": days}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    prices = response.json()["prices"]

    df = pd.DataFrame(prices, columns=["timestamp_ms", "price_usd"])
    df["timestamp"] = pd.to_datetime(df["timestamp_ms"], unit="ms")
    return df[["timestamp", "price_usd"]]


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.title("📈 Live Cryptocurrency Market Dashboard")
st.caption(
    "Real-time data sourced from the CoinGecko public API. "
    "Auto-refreshes every 60 seconds."
)

with st.sidebar:
    st.header("Settings")
    selected_coins = st.multiselect(
        "Coins to track",
        options=DEFAULT_COINS + ["polkadot", "litecoin", "chainlink"],
        default=DEFAULT_COINS,
    )
    trend_coin = st.selectbox("Coin for trend chart", options=selected_coins or DEFAULT_COINS)
    trend_days = st.slider("Trend window (days)", 1, 30, 7)
    auto_refresh = st.checkbox("Auto-refresh every 60s", value=True)

if not selected_coins:
    st.warning("Select at least one coin from the sidebar.")
    st.stop()

try:
    market_df = fetch_market_data(selected_coins)
except Exception as e:
    st.error(f"Could not fetch live data right now: {e}")
    st.stop()

# --- KPI row -----------------------------------------------------------
kpi_cols = st.columns(len(market_df))
for col, (_, row) in zip(kpi_cols, market_df.iterrows()):
    delta_color = "normal" if row["change_24h_%"] >= 0 else "inverse"
    col.metric(
        label=f"{row['name']} ({row['symbol'].upper()})",
        value=f"${row['price_usd']:,.2f}",
        delta=f"{row['change_24h_%']:.2f}% (24h)",
    )

st.divider()

# --- Table ---------------------------------------------------------------
st.subheader("Market Snapshot")
st.dataframe(
    market_df.style.format(
        {
            "price_usd": "${:,.2f}",
            "market_cap": "${:,.0f}",
            "volume_24h": "${:,.0f}",
            "change_1h_%": "{:.2f}%",
            "change_24h_%": "{:.2f}%",
            "change_7d_%": "{:.2f}%",
        }
    ),
    use_container_width=True,
)

# --- Market cap bar chart -------------------------------------------------
left, right = st.columns(2)
with left:
    st.subheader("Market Cap Comparison")
    fig_mc = px.bar(
        market_df.sort_values("market_cap", ascending=False),
        x="name",
        y="market_cap",
        color="name",
        labels={"market_cap": "Market Cap (USD)", "name": "Coin"},
    )
    st.plotly_chart(fig_mc, use_container_width=True)

with right:
    st.subheader("24h % Change")
    fig_chg = px.bar(
        market_df.sort_values("change_24h_%"),
        x="name",
        y="change_24h_%",
        color="change_24h_%",
        color_continuous_scale=["red", "green"],
        labels={"change_24h_%": "24h Change (%)", "name": "Coin"},
    )
    st.plotly_chart(fig_chg, use_container_width=True)

# --- Trend line chart -------------------------------------------------
st.subheader(f"{trend_coin.title()} Price Trend ({trend_days}d)")
try:
    history_df = fetch_price_history(trend_coin, days=trend_days)
    fig_trend = go.Figure()
    fig_trend.add_trace(
        go.Scatter(
            x=history_df["timestamp"],
            y=history_df["price_usd"],
            mode="lines",
            name=trend_coin,
            line=dict(width=2),
        )
    )
    fig_trend.update_layout(
        xaxis_title="Time", yaxis_title="Price (USD)", height=400
    )
    st.plotly_chart(fig_trend, use_container_width=True)
except Exception as e:
    st.info(f"Trend data unavailable right now: {e}")

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- Auto refresh -------------------------------------------------
if auto_refresh:
    time.sleep(60)
    st.rerun()
