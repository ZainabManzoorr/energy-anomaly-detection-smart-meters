import streamlit as st
from pathlib import Path

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="VoltSense Dashboard",
    layout="wide"
)

st.title("⚡ VoltSense – Energy Intelligence Dashboard")

# -------------------------
# PATH SETUP
# -------------------------
BASE_DIR = Path(__file__).resolve().parent
PLOT_DIR = BASE_DIR / "outputs" / "plots"

# -------------------------
# CHECK FILES EXIST
# -------------------------
def get_plot(file_name):
    path = PLOT_DIR / file_name
    if path.exists():
        return str(path)
    else:
        return None

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("📊 Navigation")

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

    col1.metric("Total Records", "Preprocessed")
    col2.metric("Total Houses", "21")
    col3.metric("Days Analyzed", "Available")

    st.divider()

    st.subheader("Daily Energy Trend")

    img = get_plot("daily_total_energy.png")
    if img:
        st.image(img)
    else:
        st.warning("daily_total_energy.png not found")

# -------------------------
# TRENDS
# -------------------------
elif page == "Trends":

    st.header("Energy Trends")

    st.subheader("Daily Total Energy")
    img = get_plot("daily_total_energy.png")
    if img:
        st.image(img)

    st.subheader("Daily Average Energy")
    img = get_plot("daily_average_energy.png")
    if img:
        st.image(img)

    st.subheader("Hourly Pattern")
    img = get_plot("hourly_energy_pattern.png")
    if img:
        st.image(img)

# -------------------------
# PATTERNS
# -------------------------
elif page == "Patterns":

    st.header("🔍 Consumption Patterns")

    st.subheader("House Comparison")
    img = get_plot("house_comparison.png")
    if img:
        st.image(img)

    st.subheader("Weekend vs Weekday")
    img = get_plot("weekend_vs_weekday.png")
    if img:
        st.image(img)

# -------------------------
# INSIGHTS
# -------------------------
elif page == "Insights":

    st.header("🧠 Insights Dashboard")

    st.success("Energy usage shows strong daily cyclic behavior.")
    st.info("Peak consumption typically occurs during evening hours.")
    st.warning("Certain houses consume significantly more energy than others.")

    st.divider()

    st.subheader("🚨 Anomaly Detection")

    img = get_plot("daily_anomalies.png")
    if img:
        st.image(img)
    else:
        st.error("Anomaly plot not found")