import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    df = pd.read_csv("dataset/main_crypto_dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def render():
    st.title(" Cryptocurrency Correlation Analysis")

    df = load_data()

   
    returns_df = (
        df.pivot(index="Date", columns="Symbol", values="Daily_Return")
        .dropna()
    )

    corr_matrix = returns_df.corr()

 
    st.subheader("Correlation Heatmap (All Cryptocurrencies)")

    heatmap_fig = px.imshow(
        corr_matrix,
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        aspect="auto"
    )

    heatmap_fig.update_layout(
        height=650,
        xaxis_title="Cryptocurrency",
        yaxis_title="Cryptocurrency"
    )

    st.plotly_chart(heatmap_fig, use_container_width=True)


    st.subheader("Correlation Insights for Selected Coin")

    selected_coin = st.selectbox(
        "Select Cryptocurrency",
        sorted(corr_matrix.columns),
        key="corr_coin_select"
    )

    coin_corr = (
        corr_matrix[selected_coin]
        .drop(selected_coin)
        .sort_values(ascending=False)
    )

    
    top_positive = (
        coin_corr.head(4)
        .reset_index()
        .rename(columns={"index": "Coin B", selected_coin: "Correlation"})
    )

    st.markdown("### 🔵 Top Positively Correlated Coins")
    st.dataframe(top_positive, use_container_width=True)

  
    negative_corr = coin_corr[coin_corr < 0]

    if len(negative_corr) >= 1:
        top_negative = (
            negative_corr.sort_values()
            .head(4)
            .reset_index()
            .rename(columns={"index": "Coin B", selected_coin: "Correlation"})
        )

        st.markdown("### 🔴 Top Negatively Correlated Coins")
        st.dataframe(top_negative, use_container_width=True)

    else:
        least_corr = (
            coin_corr.abs()
            .sort_values()
            .head(4)
            .reset_index()
            .rename(columns={"index": "Coin B", selected_coin: "Correlation"})
        )

        st.markdown("### 🟡 Least Correlated Coins")
        st.info(
            "No strongly negative correlations observed. "
            "This is common in cryptocurrency markets where assets tend to move together "
            "due to overall market sentiment."
        )

        st.dataframe(least_corr, use_container_width=True)
