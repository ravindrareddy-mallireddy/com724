# =====================================================
# FORECASTING PAGE (STREAMLIT + PLOTLY)
# =====================================================

import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# =====================================================
# Render function
# =====================================================
def render():

    st.set_page_config(page_title="Forecasting", layout="wide")
    st.title("Cryptocurrency Price Forecasting")

    # =====================================================
    # Paths
    # =====================================================
    BASE_DIR = "dataset"
    MODELS_DIR = os.path.join(BASE_DIR, "models")

    DATASET_PATH = os.path.join(BASE_DIR, "main_crypto_dataset.csv")
    REP_PATH = os.path.join(BASE_DIR, "cluster_representatives.csv")

    # =====================================================
    # Load data
    # =====================================================
    main_df = pd.read_csv(DATASET_PATH)
    main_df["Date"] = pd.to_datetime(main_df["Date"])

    rep_df = pd.read_csv(REP_PATH)
    coin_list = rep_df["Selected_Coin"].tolist()

    # =====================================================
    # Controls
    # =====================================================
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_coin = st.selectbox("Select Coin", coin_list)

    with col2:
        selected_model = st.selectbox(
            "Select Model",
            ["ARIMA", "LSTM", "Random Forest", "XGBoost", "Prophet"]
        )

    with col3:
        horizon_label = st.selectbox(
            "Select Forecast Horizon",
            ["1 Day", "7 Days", "1 Month", "3 Months"]
        )

    # =====================================================
    # Horizon mapping
    # =====================================================
    horizon_map = {
        "1 Day": 1,
        "7 Days": 7,
        "1 Month": 30,
        "3 Months": 90
    }
    horizon_days = horizon_map[horizon_label]

    # =====================================================
    # Model filename mapping
    # =====================================================
    model_prefix = {
        "ARIMA": "arima",
        "LSTM": "lstm",
        "Random Forest": "rf",
        "XGBoost": "xgb",
        "Prophet": "prophet"
    }[selected_model]

    # =====================================================
    # Actual prices
    # =====================================================
    coin_actual = (
        main_df[main_df["Symbol"] == selected_coin]
        .sort_values("Date")
        .copy()
    )

    # =====================================================
    # Predicted prices (historical)
    # =====================================================
    pred_df = pd.read_csv(
        os.path.join(MODELS_DIR, f"{model_prefix}_{selected_coin}_predicted.csv")
    )
    pred_df["Date"] = pd.to_datetime(pred_df["Date"])

    # =====================================================
    # Forecast prices
    # =====================================================
    forecast_df = pd.read_csv(
        os.path.join(MODELS_DIR, f"{model_prefix}_{selected_coin}_3_month_forecast.csv")
    )
    forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])
    forecast_df = forecast_df.iloc[:horizon_days]

    # =====================================================
    # Plotly figure
    # =====================================================
    fig = go.Figure()

    # Actual prices
    fig.add_trace(go.Scatter(
        x=coin_actual["Date"],
        y=coin_actual["Close"],
        mode="lines",
        name="Actual Price",
        line=dict(color="black")
    ))

    # Predicted prices
    fig.add_trace(go.Scatter(
        x=pred_df["Date"],
        y=pred_df["Predicted_Close"],
        mode="lines",
        name="Predicted Price (Historical)",
        line=dict(color="blue", dash="dash")
    ))

    # Forecast prices
    fig.add_trace(go.Scatter(
        x=forecast_df["Date"],
        y=forecast_df.iloc[:, 1],
        mode="lines+markers",
        name="Forecast Price",
        line=dict(color="red")
    ))

    # =====================================================
    # Layout + range selector
    # =====================================================
    fig.update_layout(
        title=f"{selected_model} Forecast for {selected_coin}",
        xaxis_title="Date",
        yaxis_title="Close Price",
        hovermode="x unified",
        template="plotly_white",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1D", step="day", stepmode="backward"),
                    dict(count=7, label="7D", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all", label="ALL")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # Forecast table
    # =====================================================
    st.subheader("Forecast Values")
    st.dataframe(forecast_df.reset_index(drop=True))
