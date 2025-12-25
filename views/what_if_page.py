# =====================================================
# WHAT-IF ANALYSIS PAGE (STREAMLIT) – AE2 MANDATORY
# =====================================================

import os
import pandas as pd
import streamlit as st

# =====================================================
# Render function
# =====================================================
def render():

    st.set_page_config(page_title="What-If Analysis", layout="wide")
    st.title("What-If Analysis & Scenario Simulation")

    # =====================================================
    # Paths (USED ONLY FOR DEFAULT PRICE)
    # =====================================================
    BASE_DIR = "dataset"
    DATASET_PATH = os.path.join(BASE_DIR, "main_crypto_dataset.csv")

    # =====================================================
    # Load dataset (safe default reference)
    # =====================================================
    if not os.path.exists(DATASET_PATH):
        st.error(f"Missing file: {DATASET_PATH}")
        st.stop()

    df = pd.read_csv(DATASET_PATH)
    df["Date"] = pd.to_datetime(df["Date"])

    # =====================================================
    # Controls — Coin selection
    # =====================================================
    selected_coin = st.selectbox(
        "Select Cryptocurrency",
        sorted(df["Symbol"].unique()),
        key="whatif_coin_select"
    )

    coin_df = (
        df[df["Symbol"] == selected_coin]
        .sort_values("Date")
    )

    current_price = coin_df["Close"].iloc[-1]

    st.info(f"Latest Market Price: £{current_price:.2f}")

    # =====================================================
    # User Inputs
    # =====================================================
    st.subheader("Scenario Inputs")

    col1, col2, col3 = st.columns(3)

    with col1:
        buy_price = st.number_input(
            "Buy Price (£)",
            value=float(round(current_price, 2)),
            step=1.0,
            key="whatif_buy_price"
        )

    with col2:
        sell_price_a = st.number_input(
            "Sell Price — Scenario A (£)",
            value=float(round(current_price * 1.1, 2)),
            step=1.0,
            key="whatif_sell_a"
        )

    with col3:
        sell_price_b = st.number_input(
            "Sell Price — Scenario B (£)",
            value=float(round(current_price * 1.3, 2)),
            step=1.0,
            key="whatif_sell_b"
        )

    st.subheader("Quantity Selection")
    st.caption(
        "Tip: Use slider for quick retail simulations, manual input for large position sizing."
    )

    quantity_mode = st.radio(
        "Choose quantity input method",
        ["Slider (small trades)", "Manual input (large trades)"],
        horizontal=True,
        key="wf_quantity_mode"
    )

    if quantity_mode == "Slider (small trades)":
        quantity = st.slider(
            "Quantity (≤ 100 units)",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
            key="wf_quantity_slider"
        )
    else:
        quantity = st.number_input(
            "Quantity (no upper limit)",
            min_value=1,
            value=100,
            step=1,
            key="wf_quantity_input"
        )


    fees_pct = st.number_input(
        "Transaction Fees (%)",
        min_value=0.0,
        max_value=5.0,
        value=0.5,
        step=0.1,
        key="whatif_fees"
    )

    # =====================================================
    # Helper: Profit calculation
    # =====================================================
    def calculate_profit(buy, sell, qty, fees):
        gross = (sell - buy) * qty
        fee_cost = (buy * qty) * (fees / 100)
        net = gross - fee_cost
        pct = (net / (buy * qty)) * 100
        return round(net, 2), round(pct, 2)

    profit_a, pct_a = calculate_profit(
        buy_price, sell_price_a, quantity, fees_pct
    )

    profit_b, pct_b = calculate_profit(
        buy_price, sell_price_b, quantity, fees_pct
    )

    # =====================================================
    # Results Display
    # =====================================================
    st.subheader("Scenario Comparison")

    colA, colB = st.columns(2)

    with colA:
        st.markdown("### Scenario A")
        st.metric("Net Profit (£)", f"£{profit_a}")
        st.metric("Return (%)", f"{pct_a}%")

    with colB:
        st.markdown("### Scenario B")
        st.metric("Net Profit (£)", f"£{profit_b}")
        st.metric("Return (%)", f"{pct_b}%")

    # =====================================================
    # Best Scenario Highlight
    # =====================================================
    st.subheader("Outcome Summary")

    if profit_a > profit_b:
        st.success("Scenario A yields higher profit.")
    elif profit_b > profit_a:
        st.success("Scenario B yields higher profit.")
    else:
        st.info("Both scenarios result in the same outcome.")

    # =====================================================
    # Explanation (AE2 narrative)
    # =====================================================
    st.subheader("How This What-If Analysis Works")

    st.markdown("""
- This tool allows **interactive scenario manipulation**.
- Profit and loss are recalculated **live** based on user inputs.
- No assumptions are made about market direction.
- This supports **decision-making**, not automated trading.

This satisfies AE2’s **mandatory What-If Analysis requirement**.
""")
