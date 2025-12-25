# =====================================================
# TRADING SIGNALS PAGE (STREAMLIT) – FIXED IDS
# =====================================================

import os
import pandas as pd
import streamlit as st

# =====================================================
# Render function
# =====================================================
def render():

    st.set_page_config(page_title="Trading Signals", layout="wide")
    st.title("Trading Signals & Decision Support")

    # =====================================================
    # Paths (UNCHANGED)
    # =====================================================
    BASE_DIR = "dataset"
    MODELS_DIR = os.path.join(BASE_DIR, "models")

    SIGNALS_PATH = os.path.join(
        MODELS_DIR, "trading_signals.csv"
    )

    # =====================================================
    # Load data
    # =====================================================
    if not os.path.exists(SIGNALS_PATH):
        st.error(f"Missing file: {SIGNALS_PATH}")
        st.stop()

    signals_df = pd.read_csv(SIGNALS_PATH)

    # =====================================================
    # Controls (INSIDE PAGE) — FIXED WITH UNIQUE KEYS
    # =====================================================
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

    # =====================================================
    # Filter data
    # =====================================================
    filtered_df = signals_df[
        (signals_df["Symbol"] == selected_coin) &
        (signals_df["Horizon"] == selected_horizon)
    ].copy()

    if filtered_df.empty:
        st.warning("No trading signals available.")
        return

    # =====================================================
    # Confidence logic
    # =====================================================
    def confidence_level(row):
        ret = abs(row["Expected_Return_%"])
        if ret >= 8:
            return "High"
        elif ret >= 4:
            return "Medium"
        else:
            return "Low"

    filtered_df["Confidence"] = filtered_df.apply(
        confidence_level, axis=1
    )

    # =====================================================
    # Signal color mapping
    # =====================================================
    def signal_color(signal):
        if signal == "BUY":
            return "🟢 BUY"
        elif signal == "SELL":
            return "🔴 SELL"
        else:
            return "⚪ HOLD"

    filtered_df["Signal_Display"] = filtered_df["Signal"].apply(signal_color)

    # =====================================================
    # Display results
    # =====================================================
    st.subheader(
        f"Generated Trading Signals — {selected_coin} ({selected_horizon})"
    )

    for _, row in filtered_df.iterrows():

        st.markdown("---")
        col1, col2, col3 = st.columns(3)

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

        st.markdown(
            f"""
**Entry Price:** £{row['Entry_Price']}  
**Exit Price:** £{row['Exit_Price']}  
**Trend Direction:** {row['Trend']}  
**Moving Average Signal:** {row['MA_Signal']}
"""
        )

    # =====================================================
    # Explanation
    # =====================================================
    st.subheader("How Signals Are Generated")

    st.markdown("""
- **BUY**: Forecast price increases by more than **+3%**
- **SELL**: Forecast price decreases by more than **−3%**
- **HOLD**: Price movement within threshold
- **Confidence** is based on return magnitude
- **Trend confirmation** uses moving averages

This tab converts forecasts into **actionable decision support**, as required by AE2.
""")
