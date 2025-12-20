import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def render():

    # ======================================
    # Load dataset
    # ======================================
    @st.cache_data
    def load_data():
        return pd.read_csv(
            "dataset/main_crypto_dataset.csv",
            parse_dates=["Date"]
        ).sort_values("Date")

    df = load_data()

    st.title("📊 Exploratory Data Analysis (EDA)")
    st.markdown(
        "Explore price behaviour, return distributions, volatility, "
        "volume patterns, and summary statistics for each cryptocurrency."
    )
    st.divider()

    # ======================================
    # Dropdowns (WITH UNIQUE KEYS)
    # ======================================
    col1, col2 = st.columns(2)

    with col1:
        coin = st.selectbox(
            "Select Cryptocurrency",
            sorted(df["Symbol"].unique()),
            key="eda_coin_select"
        )

    with col2:
        eda_type = st.selectbox(
            "Select EDA View",
            [
                "Price Over Time",
                "Daily Return Distribution",
                "Log Return Distribution",
                "Volatility Analysis",
                "Volume Analysis",
                "Summary Statistics",
                "Missing Values"
            ],
            key="eda_view_select"
        )

    coin_df = df[df["Symbol"] == coin].copy()
    st.divider()

    # ======================================
    # EDA VIEWS
    # ======================================
    if eda_type == "Price Over Time":

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=coin_df["Date"],
            y=coin_df["Close"],
            mode="lines",
            name="Close Price"
        ))

        fig.update_layout(
            title=f"{coin} – Price Over Time",
            xaxis_title="Date",
            yaxis_title="Price",
            hovermode="x unified",
            dragmode="zoom"
        )

        fig.update_yaxes(fixedrange=False)
        st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})

    # --------------------------------------------------
    elif eda_type == "Daily Return Distribution":

        fig = px.histogram(
            coin_df,
            x="Daily_Return",
            nbins=100,
            title=f"{coin} – Daily Return Distribution"
        )

        fig.update_layout(
            xaxis_title="Daily Return",
            yaxis_title="Frequency"
        )

        st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------
    elif eda_type == "Log Return Distribution":

        fig = px.histogram(
            coin_df,
            x="Log_Return",
            nbins=100,
            title=f"{coin} – Log Return Distribution"
        )

        fig.update_layout(
            xaxis_title="Log Return",
            yaxis_title="Frequency"
        )

        st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------
    elif eda_type == "Volatility Analysis":

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=coin_df["Date"],
            y=coin_df["Volatility_7"],
            name="7-Day Volatility"
        ))

        fig.add_trace(go.Scatter(
            x=coin_df["Date"],
            y=coin_df["Volatility_14"],
            name="14-Day Volatility"
        ))

        fig.update_layout(
            title=f"{coin} – Rolling Volatility",
            xaxis_title="Date",
            yaxis_title="Volatility",
            hovermode="x unified",
            dragmode="zoom"
        )

        fig.update_yaxes(fixedrange=False)
        st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})

    # --------------------------------------------------
    elif eda_type == "Volume Analysis":

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=coin_df["Date"],
            y=coin_df["Volume"],
            name="Volume"
        ))

        fig.update_layout(
            title=f"{coin} – Trading Volume",
            xaxis_title="Date",
            yaxis_title="Volume",
            hovermode="x unified",
            dragmode="zoom"
        )

        fig.update_yaxes(fixedrange=False)
        st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})

    # --------------------------------------------------
    elif eda_type == "Summary Statistics":

        stats_df = (
            coin_df[
                ["Open", "High", "Low", "Close",
                 "Volume", "Daily_Return", "Log_Return"]
            ]
            .describe()
            .T
        )

        st.subheader(f"{coin} – Summary Statistics")
        st.dataframe(stats_df)

    # --------------------------------------------------
    elif eda_type == "Missing Values":

        missing_df = (
            coin_df.isnull()
            .sum()
            .reset_index()
            .rename(columns={"index": "Feature", 0: "Missing Count"})
        )

        st.subheader(f"{coin} – Missing Values")
        st.dataframe(missing_df)
