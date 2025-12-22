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


# -------------------------------------------------
# Top navigation tabs
# -------------------------------------------------
tabs = st.tabs([
    "🏠 Landing",
    "📈 EDA",
    "🔗 Correlation",
    "🧩 Clustering",
    "📈 Forecasting"
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
