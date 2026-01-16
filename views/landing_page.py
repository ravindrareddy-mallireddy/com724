import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render():

    
    @st.cache_data
    def load_data():
        return pd.read_csv(
            "dataset/main_crypto_dataset.csv",
            parse_dates=["Date"]
        ).sort_values("Date")

    df = load_data()

    st.title(" Cryptocurrency Analytics Dashboard")
    st.markdown(
        "Historical price behaviour, technical indicators, "
        "buy/sell signals, and trading volume."
    )
    st.divider()

    coin = st.selectbox(
        "Select Cryptocurrency",
        sorted(df["Symbol"].unique())
    )

    coin_df = df[df["Symbol"] == coin].copy()

   
    coin_df["Buy_Signal"] = (
        (coin_df["Close"] > coin_df["SMA_14"]) &
        (coin_df["Close"].shift(1) <= coin_df["SMA_14"].shift(1))
    )

    coin_df["Sell_Signal"] = (
        (coin_df["Close"] < coin_df["SMA_14"]) &
        (coin_df["Close"].shift(1) >= coin_df["SMA_14"].shift(1))
    )

    plot_df = coin_df.dropna(
        subset=["SMA_7", "SMA_14", "EMA_7", "EMA_14"]
    )

    x_min = plot_df["Date"].min()
    x_max = plot_df["Date"].max()

  
    range_selector = dict(
        buttons=[
            dict(count=1, label="1D", step="day", stepmode="backward"),
            dict(count=7, label="7D", step="day", stepmode="backward"),
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=3, label="3M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(step="all", label="ALL"),
        ]
    )

    plot_config = {"scrollZoom": True}

 
    price_fig = go.Figure()
    price_fig.add_trace(go.Scatter(
        x=plot_df["Date"],
        y=plot_df["Close"],
        mode="lines",
        name="Close Price"
    ))

    price_fig.update_layout(
        title=f"{coin} – Close Price",
        dragmode="zoom",
        hovermode="x unified",
        xaxis=dict(
            type="date",
            rangeselector=range_selector,
            rangeslider=dict(visible=True),
            range=[x_min, x_max],
            autorange=False
        ),
        yaxis_title="Price"
    )
    price_fig.update_yaxes(fixedrange=False)

    st.plotly_chart(price_fig, use_container_width=True, config=plot_config)
    st.divider()

    
    ma_fig = go.Figure()

    ma_fig.add_trace(go.Scatter(x=plot_df["Date"], y=plot_df["Close"], name="Close"))
    ma_fig.add_trace(go.Scatter(x=plot_df["Date"], y=plot_df["SMA_7"], name="SMA 7"))
    ma_fig.add_trace(go.Scatter(x=plot_df["Date"], y=plot_df["SMA_14"], name="SMA 14"))
    ma_fig.add_trace(go.Scatter(
        x=plot_df["Date"], y=plot_df["EMA_7"], name="EMA 7", line=dict(dash="dot")
    ))
    ma_fig.add_trace(go.Scatter(
        x=plot_df["Date"], y=plot_df["EMA_14"], name="EMA 14", line=dict(dash="dot")
    ))

    ma_fig.update_layout(
        title=f"{coin} – Moving Averages",
        dragmode="zoom",
        hovermode="x unified",
        xaxis=dict(
            type="date",
            rangeselector=range_selector,
            rangeslider=dict(visible=True),
            range=[x_min, x_max],
            autorange=False
        ),
        yaxis_title="Price"
    )
    ma_fig.update_yaxes(fixedrange=False)

    st.plotly_chart(ma_fig, use_container_width=True, config=plot_config)
    st.divider()

 
    signal_fig = go.Figure()

    signal_fig.add_trace(go.Candlestick(
        x=plot_df["Date"],
        open=plot_df["Open"],
        high=plot_df["High"],
        low=plot_df["Low"],
        close=plot_df["Close"],
        name="Price"
    ))

    signal_fig.add_trace(go.Scatter(
        x=plot_df.loc[plot_df["Buy_Signal"], "Date"],
        y=plot_df.loc[plot_df["Buy_Signal"], "Close"],
        mode="markers",
        name="Buy",
        marker=dict(color="green", symbol="triangle-up", size=10)
    ))

    signal_fig.add_trace(go.Scatter(
        x=plot_df.loc[plot_df["Sell_Signal"], "Date"],
        y=plot_df.loc[plot_df["Sell_Signal"], "Close"],
        mode="markers",
        name="Sell",
        marker=dict(color="red", symbol="triangle-down", size=10)
    ))

    signal_fig.update_layout(
        title=f"{coin} – Buy & Sell Signals (Candlestick)",
        dragmode="zoom",
        hovermode="x unified",
        xaxis=dict(
            type="date",
            rangeselector=range_selector,
            rangeslider=dict(visible=False),
            range=[x_min, x_max],
            autorange=False
        ),
        yaxis_title="Price"
    )
    signal_fig.update_yaxes(fixedrange=False)

    st.plotly_chart(signal_fig, use_container_width=True, config=plot_config)
    st.divider()

    
    volume_fig = go.Figure()
    volume_fig.add_trace(go.Bar(
        x=plot_df["Date"],
        y=plot_df["Volume"],
        name="Volume"
    ))

    volume_fig.update_layout(
        title=f"{coin} – Trading Volume",
        dragmode="zoom",
        hovermode="x unified",
        xaxis=dict(
            type="date",
            rangeselector=range_selector,
            rangeslider=dict(visible=True),
            range=[x_min, x_max],
            autorange=False
        ),
        yaxis_title="Volume"
    )
    volume_fig.update_yaxes(fixedrange=False)

    st.plotly_chart(volume_fig, use_container_width=True, config=plot_config)
