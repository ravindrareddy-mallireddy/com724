import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np

def render():

    st.set_page_config(page_title="Forecasting", layout="wide")
    st.title("Cryptocurrency Price Forecasting")

    BASE_DIR = "dataset"
    MODELS_DIR = os.path.join(BASE_DIR, "models")

    DATASET_PATH = os.path.join(BASE_DIR, "main_crypto_dataset.csv")
    REP_PATH = os.path.join(BASE_DIR, "cluster_representatives.csv")

    main_df = pd.read_csv(DATASET_PATH)
    main_df["Date"] = pd.to_datetime(main_df["Date"])

    rep_df = pd.read_csv(REP_PATH)
    coin_list = rep_df["Selected_Coin"].tolist()

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

    horizon_days = {
        "1 Day": 1,
        "7 Days": 7,
        "1 Month": 30,
        "3 Months": 90
    }[horizon_label]

    model_prefix = {
        "ARIMA": "arima",
        "LSTM": "lstm",
        "Random Forest": "rf",
        "XGBoost": "xgb",
        "Prophet": "prophet"
    }[selected_model]

    if "Symbol" in main_df.columns:
        coin_actual = main_df[main_df["Symbol"] == selected_coin].sort_values("Date").copy()
    else:
        coin_actual = main_df.sort_values("Date").copy()

    pred_df = pd.read_csv(
        os.path.join(MODELS_DIR, f"{model_prefix}_{selected_coin}_predicted.csv")
    )
    pred_df["Date"] = pd.to_datetime(pred_df["Date"])

    forecast_df = pd.read_csv(
        os.path.join(MODELS_DIR, f"{model_prefix}_{selected_coin}_3_month_forecast.csv")
    )
    forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])
    forecast_df = forecast_df.iloc[:horizon_days]

    eval_df = pd.merge(
        coin_actual[["Date", "Close"]],
        pred_df[["Date", "Predicted_Close"]],
        on="Date",
        how="inner"
    )

    residuals = eval_df["Close"] - eval_df["Predicted_Close"]
    error_std = residuals.std()

    mape = np.mean(np.abs(residuals / eval_df["Close"])) * 100
    confidence = max(0, 100 - mape)

    if confidence >= 85:
        confidence_label = "High"
    elif confidence >= 70:
        confidence_label = "Medium"
    else:
        confidence_label = "Low"

    st.markdown(
        f"""
        **Model Confidence:** {confidence:.2f}%  
        **Confidence Level:** {confidence_label}  
        *(Confidence bands represent forecast uncertainty)*
        """
    )

    forecast_values = forecast_df.iloc[:, 1]
    upper_band = forecast_values + error_std
    lower_band = forecast_values - error_std

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=coin_actual["Date"],
        y=coin_actual["Close"],
        mode="lines",
        name="Actual Price",
        line=dict(color="black")
    ))

    fig.add_trace(go.Scatter(
        x=pred_df["Date"],
        y=pred_df["Predicted_Close"],
        mode="lines",
        name="Predicted Price (Historical)",
        line=dict(color="blue", dash="dash")
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df["Date"],
        y=forecast_values,
        mode="lines+markers",
        name="Forecast Price",
        line=dict(color="red")
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df["Date"],
        y=upper_band,
        mode="lines",
        name="Upper Confidence Bound",
        line=dict(width=0),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df["Date"],
        y=lower_band,
        mode="lines",
        name="Lower Confidence Bound",
        fill="tonexty",
        fillcolor="rgba(255,0,0,0.15)",
        line=dict(width=0),
        showlegend=False
    ))

    fig.update_layout(
        title=f"{selected_model} Forecast for {selected_coin}",
        xaxis_title="Date",
        yaxis_title="Close Price",
        hovermode="x unified",
        template="plotly_white",
        xaxis=dict(
            rangeselector=dict(
                buttons=[
                    dict(count=1, label="1D", step="day", stepmode="backward"),
                    dict(count=7, label="7D", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all", label="ALL")
                ]
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Forecast Values")
    st.dataframe(forecast_df.reset_index(drop=True))
