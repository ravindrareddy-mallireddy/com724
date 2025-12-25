import streamlit as st

# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="COM724 Crypto Analytics",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# Import page render functions
# -------------------------------------------------
from views.landing_page import render as landing_page
from views.eda_page import render as eda_page
from views.correlation_page import render as correlation_page
from views.clustering_page import render as clustering_page
from views.forecasting_page import render as forecasting_page
from views.model_comparision_page import render as model_comparision_page
from views.trading_signals_page import render as trading_signals_page
from views.what_if_page import render as what_if_page
from views.profit_target_finder_page import render as profit_target_finder_page


# -------------------------------------------------
# Top navigation tabs
# -------------------------------------------------
tabs = st.tabs([
    "🏠 Landing",
    "📈 EDA",
    "🔗 Correlation",
    "🧩 Clustering",
    "📈 Forecasting",
    "📈 Model Comparison",
    "📈 Trading Signals",
    "📈 What-If Analysis",
    "📈 Profit Target Finder"

])

# -------------------------------------------------
# Route tabs to pages
# -------------------------------------------------
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