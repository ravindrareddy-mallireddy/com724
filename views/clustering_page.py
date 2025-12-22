import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
DATA_PATH = "dataset/main_crypto_dataset.csv"
PCA_PATH = "dataset/pca_components.csv"
CLUSTER_PATH = "dataset/clustered_coins.csv"
REPRESENTATIVE_PATH = "dataset/cluster_representatives.csv"

NO_CORRELATION_COINS = []

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_main_data():
    return pd.read_csv(DATA_PATH, parse_dates=["Date"])

@st.cache_data
def load_pca_data():
    return pd.read_csv(PCA_PATH)

@st.cache_data
def load_cluster_data():
    return pd.read_csv(CLUSTER_PATH)

@st.cache_data
def load_representatives():
    return pd.read_csv(REPRESENTATIVE_PATH)

# --------------------------------------------------
# PAGE RENDER
# --------------------------------------------------
def render():
    st.title("Clustering Analysis")

    df = load_main_data()
    pca_df = load_pca_data()
    cluster_df = load_cluster_data()
    rep_df = load_representatives()

    # --------------------------------------------------
    # SECTION 1: REPRESENTATIVE COINS
    # --------------------------------------------------
    st.subheader("Selected Representative Coins (One per Cluster)")

    st.dataframe(
        rep_df.rename(columns={"Selected_Coin": "Representative Coin"}),
        use_container_width=True
    )

    st.info(
        "One cryptocurrency was selected from each cluster based on minimum "
        "distance to the cluster centroid in PCA space. These coins represent "
        "the typical behaviour of their respective clusters."
    )

    # --------------------------------------------------
    # SECTION 2: PCA CLUSTERING VISUALISATION
    # --------------------------------------------------
    st.subheader("Cryptocurrency Clusters (PCA Projection)")

    fig_cluster = px.scatter(
        pca_df,
        x="PC1",
        y="PC2",
        color="Cluster",
        hover_data=["Symbol"],
        title="K-Means Clustering in PCA-Reduced Feature Space"
    )

    st.plotly_chart(fig_cluster, use_container_width=True)

    # --------------------------------------------------
    # SECTION 3: CORRELATION INSIGHT (REPRESENTATIVES ONLY)
    # --------------------------------------------------
    st.subheader("Correlation Insight (Representative Coins Only)")

    selected_coin = st.selectbox(
        "Select a Representative Coin",
        rep_df["Selected_Coin"].tolist(),
        key="cluster_corr_coin"
    )

    # --------------------------------------------------
    # SPECIAL CASE: NO VALID CORRELATION
    # --------------------------------------------------
    if selected_coin in NO_CORRELATION_COINS:
        st.info(
            f"**Correlation not shown for {selected_coin}.**\n\n"
            "This cryptocurrency exhibits highly idiosyncratic or extreme return "
            "behaviour. As a result, statistically meaningful Pearson correlation "
            "coefficients cannot be reliably computed.\n\n"
            "This does not affect its validity in clustering, where distance-based "
            "similarity is used instead of correlation."
        )
        return

    # --------------------------------------------------
    # CORRELATION LOGIC (SAME AS CORRELATION PAGE)
    # --------------------------------------------------
    returns_df = (
        df.pivot(index="Date", columns="Symbol", values="Daily_Return")
        .dropna(how="any")
    )

    if selected_coin not in returns_df.columns:
        st.warning("Selected coin not available for correlation analysis.")
        return

    corr_series = returns_df.corr()[selected_coin].drop(selected_coin)

    # Top positive correlations
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
            "This is common in cryptocurrency markets due to shared "
            "market-wide influences."
        )

    # --------------------------------------------------
    # DISPLAY RESULTS
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
