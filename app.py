<details>
<summary><strong>📄 Paste this into app.py</strong></summary>
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="ASX Small Cap Swing Tracker", layout="wide")

st.title("📊 ASX Small Cap Daily Swing Tracker")

# Sample ASX small cap tickers
asx_small_caps = [
    "AVZ.AX", "CXO.AX", "SYA.AX", "VUL.AX", "EMN.AX",
    "INR.AX", "LTR.AX", "GL1.AX", "RNU.AX", "PNN.AX"
]

# User-selectable tickers
selected_tickers = st.multiselect("Select ASX small cap tickers:", asx_small_caps, default=asx_small_caps)

if selected_tickers:
    # Fetch data
    data = yf.download(selected_tickers, period="5d", interval="1d", group_by='ticker', auto_adjust=False)

    swing_results = []

    for ticker in selected_tickers:
        if ticker in data:
            df = data[ticker].dropna()
            if not df.empty:
                latest = df.iloc[-1]
                open_price = latest['Open']
                high_price = latest['High']
                low_price = latest['Low']
                close_price = latest['Close']
                if open_price > 0:
                    swing_percent = ((high_price - low_price) / open_price) * 100
                    swing_results.append({
                        'Ticker': ticker,
                        'Open': open_price,
                        'High': high_price,
                        'Low': low_price,
                        'Close': close_price,
                        'Swing %': round(swing_percent, 2)
                    })

    # Display swing data
    swing_df = pd.DataFrame(swing_results).sort_values(by="Swing %", ascending=False)
    st.subheader("🔝 Top Daily Movers by Swing %")
    st.dataframe(swing_df)

    # Charts
    st.subheader("📈 Price Charts")
    for ticker in swing_df["Ticker"]:
        df = data[ticker].dropna()
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name=ticker
        )])
        fig.update_layout(title=ticker, xaxis_title="Date", yaxis_title="Price (AUD)", height=300)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please select at least one ticker.")
</details>
