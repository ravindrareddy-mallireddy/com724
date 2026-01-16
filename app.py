import streamlit as st


st.set_page_config(
    page_title="COM724 Crypto Analytics",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>

/* ---------- TAB BAR CONTAINER ---------- */
div[data-testid="stTabs"] {
    background-color: #0e1117;
    padding: 12px 16px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

/* ---------- TAB LIST ---------- */
div[data-testid="stTabs"] > div {
    gap: 8px;
}

/* ---------- INDIVIDUAL TAB ---------- */
button[data-baseweb="tab"] {
    background-color: #111827;
    color: #9ca3af;
    border-radius: 8px;
    padding: 8px 14px;
    border: 1px solid transparent;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.25s ease-in-out;
}

/* ---------- HOVER ---------- */
button[data-baseweb="tab"]:hover {
    background-color: #1f2937;
    color: #ffffff;
}

/* ---------- ACTIVE TAB ---------- */
button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #2563eb;
    color: #ffffff;
    border: 1px solid #3b82f6;
    box-shadow: 0 0 0 1px rgba(59,130,246,0.4);
}

/* ---------- REMOVE DEFAULT UNDERLINE ---------- */
button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
    margin-bottom: 0;
}

</style>
""", unsafe_allow_html=True)


from views.landing_page import render as landing_page
from views.eda_page import render as eda_page
from views.correlation_page import render as correlation_page
from views.clustering_page import render as clustering_page
from views.forecasting_page import render as forecasting_page
from views.model_comparision_page import render as model_comparision_page
from views.trading_signals_page import render as trading_signals_page
from views.what_if_page import render as what_if_page
from views.profit_target_finder_page import render as profit_target_finder_page
from views.crypto_news import render as crypto_news_page



tabs = st.tabs([
    " Landing",
    " EDA",
    " Correlation",
    " Clustering",
    " Forecasting",
    " Model Comparison",
    " Trading Signals",
    " What-If Analysis",
    " Profit Target Finder",
    " Crypto News"

])


with tabs[0]:
    landing_page()

with tabs[1]:
    eda_page()

with tabs[2]:
    correlation_page()

with tabs[3]:
    clustering_page()

with tabs[4]:
    forecasting_page()

with tabs[5]:
    model_comparision_page()

with tabs[6]:
    trading_signals_page()

with tabs[7]:
    what_if_page()

with tabs[8]:
    profit_target_finder_page()

with tabs[9]:
    crypto_news_page()