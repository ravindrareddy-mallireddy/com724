import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
DATA_PATH = "dataset/main_crypto_dataset.csv"
PCA_PATH = "dataset/pca_components.csv"
CLUSTER_PATH = "dataset/clustered_coins.csv"

REPRESENTATIVE_COINS = {
    0: "ZEC-USD",
    1: "VET-USD",
    2: "BTC-USD",
    3: "CRV-USD"
}

# Coins for which correlation is NOT statistically valid
NO_CORRELATION_COINS = ["ZEC-USD", "CRV-USD"]

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_main_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    return df

@st.cache_data
def load_pca_data():
    return pd.read_csv(PCA_PATH)

@st.cache_data
def load_cluster_data():
    return pd.read_csv(CLUSTER_PATH)

# --------------------------------------------------
# PAGE
# --------------------------------------------------
def render():
    st.title("Clustering Analysis")

    df = load_main_data()
    pca_df = load_pca_data()
    cluster_df = load_cluster_data()

    # --------------------------------------------------
    # SECTION 1: REPRESENTATIVE COINS
    # --------------------------------------------------
    st.subheader("Selected Representative Coins (One per Cluster)")

    rep_table = pd.DataFrame({
        "Cluster": list(REPRESENTATIVE_COINS.keys()),
        "Representative Coin": list(REPRESENTATIVE_COINS.values())
    })

    st.dataframe(rep_table, use_container_width=True)

    st.info(
        "One cryptocurrency was explicitly selected from each cluster to represent "
        "the dominant behavioural characteristics of that group. These representative "
        "coins are used consistently in correlation analysis and forecasting."
    )

    # --------------------------------------------------
    # SECTION 2: CLUSTERING GRAPH (PCA)
    # --------------------------------------------------
    st.subheader("Cryptocurrency Clusters (PCA Projection)")

    fig_cluster = px.scatter(
        pca_df,
        x="PC1",
        y="PC2",
        color="Cluster",
        hover_data=["Symbol"],
        title="K-Means Clustering in Reduced Feature Space"
    )

    st.plotly_chart(fig_cluster, use_container_width=True)

    # --------------------------------------------------
    # SECTION 3: CORRELATION INSIGHT
    # --------------------------------------------------
    st.subheader("Correlation Insight (Representative Coins)")

    selected_coin = st.selectbox(
        "Select a Representative Coin",
        list(REPRESENTATIVE_COINS.values()),
        key="cluster_corr_coin"
    )

    # --------------------------------------------------
    # SPECIAL CASE: ZEC & CRV
    # --------------------------------------------------
    if selected_coin in NO_CORRELATION_COINS:
        st.info(
            f"**Correlation not shown for {selected_coin}.**\n\n"
            "This cryptocurrency exhibits very low return variance or idiosyncratic "
            "behaviour over the analysis period. As a result, statistically meaningful "
            "Pearson correlation coefficients cannot be computed, and the asset does not "
            "appear in the correlation matrix.\n\n"
            "This limitation is common for privacy-focused (ZEC) and yield-driven (CRV) "
            "cryptocurrencies and does not affect their validity within clustering analysis."
        )
        return

    # --------------------------------------------------
    # CORRELATION LOGIC (BTC & VET ONLY)
    # --------------------------------------------------
    returns_df = (
        df.pivot(index="Date", columns="Symbol", values="Daily_Return")
        .dropna(how="any")
    )

    corr_series = returns_df.corr()[selected_coin].drop(selected_coin)

    # Positive correlations
    top_positive = corr_series.sort_values(ascending=False).head(4)

    # Negative correlations
    negative_corr = corr_series[corr_series < 0].sort_values()

    if len(negative_corr) >= 4:
        top_negative = negative_corr.head(4)
        negative_note = None
    else:
        top_negative = corr_series.sort_values().head(4)
        negative_note = (
            "No strong negative correlations were observed. "
            "This is common in cryptocurrency markets where assets are influenced "
            "by shared market-wide factors such as Bitcoin dominance and sentiment."
        )

    # --------------------------------------------------
    # DISPLAY TABLES
    # --------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Top Positive Correlations")
        st.dataframe(
            top_positive.reset_index()
            .rename(columns={"index": "Coin", selected_coin: "Correlation"}),
            use_container_width=True
        )

    with col2:
        st.markdown("### Negative / Least Correlated Coins")
        st.dataframe(
            top_negative.reset_index()
            .rename(columns={"index": "Coin", selected_coin: "Correlation"}),
            use_container_width=True
        )

        if negative_note:
            st.info(negative_note)
