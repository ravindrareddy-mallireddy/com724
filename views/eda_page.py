import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render():
    st.title(" Exploratory Data Analysis (EDA)")

   
    df = pd.read_csv("dataset/main_crypto_dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"])

   
    coin = st.selectbox(
        "Select Cryptocurrency",
        sorted(df["Symbol"].unique()),
        key="eda_coin_select"
    )

    eda_type = st.selectbox(
        "Select EDA Type",
        [
            "Price Over Time",
            "Price with Moving Averages",
            "Daily Return Distribution",
            "Log Return Distribution",
            "Volatility Analysis",
            "Volume Analysis",
            "Summary Statistics",
            "Missing Values"
        ],
        key="eda_type_select"
    )

    coin_df = df[df["Symbol"] == coin].sort_values("Date")

    
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

   

    # -------- Price Over Time --------
    if eda_type == "Price Over Time":
        fig = px.line(
            coin_df,
            x="Date",
            y="Close",
            title=f"{coin} – Price Over Time"
        )

        fig.update_layout(
            hovermode="x unified",
            xaxis=dict(
                type="date",
                rangeselector=range_selector,
                rangeslider=dict(visible=True)
            ),
            yaxis_title="Price"
        )

        fig.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True)

    # -------- Price + Moving Averages --------
    elif eda_type == "Price with Moving Averages":
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=coin_df["Date"],
            y=coin_df["Close"],
            name="Close Price"
        ))

        fig.add_trace(go.Scatter(
            x=coin_df["Date"],
            y=coin_df["SMA_7"],
            name="SMA 7",
            line=dict(dash="dot")
        ))

        fig.add_trace(go.Scatter(
            x=coin_df["Date"],
            y=coin_df["SMA_14"],
            name="SMA 14",
            line=dict(dash="dot")
        ))

        fig.update_layout(
            title=f"{coin} – Price with Moving Averages",
            hovermode="x unified",
            xaxis=dict(
                type="date",
                rangeselector=range_selector,
                rangeslider=dict(visible=True)
            ),
            yaxis_title="Price"
        )

        fig.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True)

    # -------- Daily Return Distribution --------
    elif eda_type == "Daily Return Distribution":
        fig = px.histogram(
            coin_df,
            x="Daily_Return",
            nbins=60,
            title=f"{coin} – Daily Return Distribution"
        )

        fig.update_xaxes(zeroline=True)
        st.plotly_chart(fig, use_container_width=True)

    # -------- Log Return Distribution --------
    elif eda_type == "Log Return Distribution":
        fig = px.histogram(
            coin_df,
            x="Log_Return",
            nbins=60,
            title=f"{coin} – Log Return Distribution"
        )

        fig.update_xaxes(zeroline=True)
        st.plotly_chart(fig, use_container_width=True)

    # -------- Volatility Analysis --------
    elif eda_type == "Volatility Analysis":
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=coin_df["Date"],
            y=coin_df["Volatility_7"],
            name="Volatility 7D"
        ))

        fig.add_trace(go.Scatter(
            x=coin_df["Date"],
            y=coin_df["Volatility_14"],
            name="Volatility 14D"
        ))

        fig.update_layout(
            title=f"{coin} – Rolling Volatility",
            hovermode="x unified",
            xaxis=dict(
                type="date",
                rangeselector=range_selector,
                rangeslider=dict(visible=True)
            ),
            yaxis_title="Volatility"
        )

        fig.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True)

    # -------- Volume Analysis --------
    elif eda_type == "Volume Analysis":
        fig = px.bar(
            coin_df,
            x="Date",
            y="Volume",
            title=f"{coin} – Trading Volume"
        )

        fig.update_layout(
            hovermode="x unified",
            xaxis=dict(
                type="date",
                rangeselector=range_selector,
                rangeslider=dict(visible=True)
            ),
            yaxis_title="Volume"
        )

        fig.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True)

    # -------- Summary Statistics --------
    elif eda_type == "Summary Statistics":
        st.subheader(f"{coin} – Summary Statistics")
        st.dataframe(coin_df.describe())

    # -------- Missing Values --------
    elif eda_type == "Missing Values":
        st.subheader(f"{coin} – Missing Values")
        missing = coin_df.isna().sum().reset_index()
        missing.columns = ["Feature", "Missing Count"]
        st.dataframe(missing)
