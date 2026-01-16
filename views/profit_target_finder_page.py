

import os
import pandas as pd
import streamlit as st


def render():

    st.set_page_config(page_title="Profit Target Finder", layout="wide")
    st.title(" Profit Target Finder")

  
    BASE_DIR = "dataset"
    OUTPUTS_DIR = os.path.join(BASE_DIR, "models")
    DATA_PATH = os.path.join(OUTPUTS_DIR, "profit_target_inputs.csv")

    if not os.path.exists(DATA_PATH):
        st.error("Missing file: profit_target_inputs.csv")
        st.stop()

    df = pd.read_csv(DATA_PATH)

    
    col1, col2, col3 = st.columns(3)

    with col1:
        target_profit = st.number_input(
            "Target Profit (£)",
            min_value=10.0,
            value=300.0,
            step=10.0,
            key="profit_target_input"
        )

    with col2:
        horizon_days = st.selectbox(
            "Time Horizon",
            options=[7, 14, 30, 90],
            format_func=lambda x: f"{x} Days",
            key="profit_horizon_select"
        )

    with col3:
        capital = st.number_input(
            "Available Capital (£)",
            min_value=100.0,
            value=1000.0,
            step=50.0,
            key="capital_input"
        )

    
    df = df[df["Horizon_Days"] == horizon_days].copy()

   
    df["Units_Affordable"] = (capital / df["Current_Price"]).astype(int)
    df["Max_Possible_Profit"] = (
        df["Units_Affordable"] * df["Expected_Profit_per_Unit"]
    )

    df["Meets_Target"] = df["Max_Possible_Profit"] >= target_profit

    
    def confidence_label(ret):
        if ret >= 15:
            return "High"
        elif ret >= 7:
            return "Medium"
        else:
            return "Low"

    df["Confidence"] = df["Expected_Return_Pct"].apply(confidence_label)

    
    feasible_df = df[df["Meets_Target"]].copy()

    if feasible_df.empty:
        st.warning("⚠ No coin can meet the target profit under current constraints.")
        return

   
    feasible_df = feasible_df.sort_values(
        by=["Max_Possible_Profit", "Expected_Return_Pct"],
        ascending=False
    )


    st.subheader("Ranked Opportunities")

    display_cols = [
        "Coin",
        "Model",
        "Current_Price",
        "Forecast_Price",
        "Expected_Return_Pct",
        "Units_Affordable",
        "Max_Possible_Profit",
        "Confidence"
    ]

    st.dataframe(
        feasible_df[display_cols].reset_index(drop=True),
        use_container_width=True
    )

  
    best = feasible_df.iloc[0]

    st.markdown("---")
    st.subheader(" Suggested Trade")

    st.markdown(
        f"""
        **Coin:** {best['Coin']}  
        **Model:** {best['Model']}  
        **Buy Price:** £{best['Current_Price']}  
        **Forecast Price:** £{best['Forecast_Price']}  
        **Units:** {best['Units_Affordable']}  
        **Expected Profit:** £{round(best['Max_Possible_Profit'], 2)}  
        **Confidence:** **{best['Confidence']}**
        """
    )

   
    st.info(
        "This tool converts forecasts into profit-driven decisions, "
        "supporting realistic capital constraints and scenario-based evaluation as required in AE2."
    )
