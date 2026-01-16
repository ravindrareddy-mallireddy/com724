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

    last_hist_date = coin_actual["Date"].max()

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

    confidence_label = "High" if confidence >= 85 else "Medium" if confidence >= 70 else "Low"

    st.markdown(
        f"""
        **Model Confidence:** {confidence:.2f}%  
        **Confidence Level:** {confidence_label}  
        *(Confidence bands represent forecast uncertainty)*
        """
    )

    forecast_values = forecast_df.iloc[:, 1].values
    forecast_dates = forecast_df["Date"].values

    upper_band = forecast_values + error_std
    lower_band = forecast_values - error_std

    # ================= MULTIPLE BUY / SELL SIGNALS (ONLY CHANGE) =================
    buy_dates, buy_prices = [], []
    sell_dates, sell_prices = [], []

    for i in range(1, len(forecast_values) - 1):
        if forecast_values[i] < forecast_values[i - 1] and forecast_values[i] < forecast_values[i + 1]:
            buy_dates.append(forecast_dates[i])
            buy_prices.append(forecast_values[i])

        if forecast_values[i] > forecast_values[i - 1] and forecast_values[i] > forecast_values[i + 1]:
            sell_dates.append(forecast_dates[i])
            sell_prices.append(forecast_values[i])
    # ============================================================================

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=coin_actual["Date"],
        y=coin_actual["Close"],
        mode="lines",
        name="Actual Price",
        line=dict(color="#e5e7eb", width=2)
    ))

    fig.add_trace(go.Scatter(
        x=pred_df["Date"],
        y=pred_df["Predicted_Close"],
        mode="lines",
        name="Predicted Price (Historical)",
        line=dict(color="#3b82f6", dash="dash", width=2)
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df["Date"],
        y=forecast_values,
        mode="lines+markers",
        name="Forecast Price",
        line=dict(color="#ef4444", width=0.5),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df["Date"],
        y=upper_band,
        mode="lines",
        line=dict(color="rgba(239,68,68,0.3)"),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df["Date"],
        y=lower_band,
        mode="lines",
        fill="tonexty",
        fillcolor="rgba(239,68,68,0.18)",
        line=dict(color="rgba(239,68,68,0.3)"),
        name="Confidence Interval"
    ))

    fig.add_trace(go.Scatter(
        x=buy_dates,
        y=buy_prices,
        mode="markers",
        name="BUY Signal",
        marker=dict(color="lime", size=14, symbol="triangle-up")
    ))

    fig.add_trace(go.Scatter(
        x=sell_dates,
        y=sell_prices,
        mode="markers",
        name="SELL Signal",
        marker=dict(color="red", size=14, symbol="triangle-down")
    ))

    fig.update_layout(
        template="plotly_dark",
        title=f"{selected_model} Forecast for {selected_coin}",
        hovermode="x unified",
        height=520,

        plot_bgcolor="rgba(17,24,39,1)",
        paper_bgcolor="rgba(14,17,23,1)",

        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
            range=[coin_actual["Date"].min(), last_hist_date],
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
        ),

        yaxis=dict(
            title="Close Price",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        ),

        margin=dict(l=60, r=40, t=60, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Forecast Values")
    st.dataframe(forecast_df.reset_index(drop=True))
