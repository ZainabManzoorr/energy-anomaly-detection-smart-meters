import streamlit as st
import pandas as pd

from voltsense.ingestion.multi_loader import MultiHouseDataLoader
from voltsense.analytics.energy_analytics import EnergyAnalytics

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="VoltSense Dashboard",
    layout="wide"
)

st.title("VoltSense – Energy Intelligence Dashboard")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    loader = MultiHouseDataLoader("data/raw/refit_extracted")
    df = loader.load_all()
    return df

df = load_data()

analytics = EnergyAnalytics(df)
analytics.prepare_time_series()

daily = analytics.daily_consumption()
hourly = analytics.hourly_consumption()
houses = analytics.house_consumption()
weekend = analytics.weekend_vs_weekday()

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Overview", "Trends", "Patterns", "Insights"]
)

# -------------------------
# OVERVIEW
# -------------------------
if page == "Overview":

    st.header("Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df))
    col2.metric("Total Houses", houses.shape[0])
    col3.metric("Days Analyzed", daily.shape[0])

    st.divider()

    st.subheader("Daily Energy Trend")
    st.image("outputs/plots/daily_total_energy.png")

# -------------------------
# TRENDS
# -------------------------
elif page == "Trends":

    st.header("Energy Trends")

    st.subheader("Daily Total Energy")
    st.image("outputs/plots/daily_total_energy.png")

    st.subheader("Daily Average Energy")
    st.image("outputs/plots/daily_average_energy.png")

    st.subheader("Hourly Pattern")
    st.image("outputs/plots/hourly_energy_pattern.png")

# -------------------------
# PATTERNS
# -------------------------
elif page == "Patterns":

    st.header("Consumption Patterns")

    st.subheader("House Comparison")
    st.image("outputs/plots/house_comparison.png")

    st.subheader("Weekend vs Weekday")
    st.image("outputs/plots/weekend_vs_weekday.png")

# -------------------------
# INSIGHTS
# -------------------------
elif page == "Insights":

    st.header("Insights Dashboard")

    st.success("Energy usage shows strong daily cyclic behavior.")

    st.info("Peak consumption typically occurs during evening hours.")

    st.warning("Certain houses consume significantly more energy than others.")

    st.divider()

    st.subheader("Anomaly Detection")

    st.image("outputs/plots/daily_anomalies.png")