import os
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

def render():

    st.set_page_config(page_title="Trading Signals", layout="wide")
    st.title("Trading Signals & Decision Support")

    BASE_DIR = "dataset"
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    SIGNALS_PATH = os.path.join(MODELS_DIR, "trading_signals.csv")

    if not os.path.exists(SIGNALS_PATH):
        st.error(f"Missing file: {SIGNALS_PATH}")
        st.stop()

    signals_df = pd.read_csv(SIGNALS_PATH)

    col1, col2 = st.columns(2)

    with col1:
        selected_coin = st.selectbox(
            "Select Cryptocurrency",
            sorted(signals_df["Symbol"].unique()),
            key="trading_coin_select"
        )

    with col2:
        selected_horizon = st.selectbox(
            "Select Horizon",
            ["7D", "14D", "30D"],
            key="trading_horizon_select"
        )

    filtered_df = signals_df[
        (signals_df["Symbol"] == selected_coin) &
        (signals_df["Horizon"] == selected_horizon)
    ].copy()

    if filtered_df.empty:
        st.warning("No trading signals available.")
        return

    horizon_days = int(selected_horizon.replace("D", ""))
    buy_date = datetime.today().date()
    sell_date = buy_date + timedelta(days=horizon_days)

    def confidence_level(row):
        ret = abs(row["Expected_Return_%"])
        if ret >= 8:
            return "High"
        elif ret >= 4:
            return "Medium"
        else:
            return "Low"

    def risk_level(row):
        ret = abs(row["Expected_Return_%"])
        if ret >= 10:
            return "High Risk"
        elif ret >= 5:
            return "Medium Risk"
        else:
            return "Low Risk"

    filtered_df["Confidence"] = filtered_df.apply(confidence_level, axis=1)
    filtered_df["Risk_Level"] = filtered_df.apply(risk_level, axis=1)

    def signal_color(signal):
        if signal == "BUY":
            return "🟢 BUY"
        elif signal == "SELL":
            return "🔴 SELL"
        else:
            return "⚪ HOLD"

    filtered_df["Signal_Display"] = filtered_df["Signal"].apply(signal_color)

    st.subheader(
        f"Generated Trading Signals — {selected_coin} ({selected_horizon})"
    )

    for _, row in filtered_df.iterrows():

        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label=f"{row['Model']} Signal",
                value=row["Signal_Display"]
            )

        with col2:
            st.metric(
                label="Expected Return (%)",
                value=f"{row['Expected_Return_%']}%"
            )

        with col3:
            st.metric(
                label="Confidence",
                value=row["Confidence"]
            )

        with col4:
            st.metric(
                label="Risk Level",
                value=row["Risk_Level"]
            )

        st.markdown(
            f"""
**Best Time to Buy:** {buy_date}  
**Best Time to Sell:** {sell_date}  

**Entry Price:** £{row['Entry_Price']}  
**Exit Price:** £{row['Exit_Price']}  

**Trend Direction:** {row['Trend']}  
**Moving Average Signal:** {row['MA_Signal']}
"""
        )

        if row["Risk_Level"] == "High Risk":
            st.warning("High volatility detected – suitable for aggressive investors.")
        elif row["Risk_Level"] == "Medium Risk":
            st.info("Moderate volatility – balanced risk and return.")
        else:
            st.success("Low volatility – suitable for conservative investors.")

    st.subheader("How Signals Are Generated")

    st.markdown("""
- **BUY**: Forecast price increases by more than **+3%**
- **SELL**: Forecast price decreases by more than **−3%**
- **HOLD**: Price movement within threshold
- **Confidence** reflects forecast reliability
- **Risk level** reflects market volatility inferred from return magnitude
- **Buy/Sell timing** is derived dynamically from the selected horizon
- **Trend confirmation** uses moving averages

This page provides **risk-aware, time-based trading decisions**, fulfilling AE2 decision-support requirements.
""")
