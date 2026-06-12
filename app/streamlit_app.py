import streamlit as st
import pandas as pd

from src.utils.preprocessing import load_data, add_features
from src.anomaly_detection import generate_anomalies

st.set_page_config(page_title="VoltSense Dashboard", layout="wide")

st.title("⚡ VoltSense - Energy Anomaly Detection System")

# Load data
df = load_data("data/energy_data.csv")

# Feature engineering + anomaly pipeline
df = add_features(df)
df = generate_anomalies(df)

# Sidebar filter
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df["day"].min())
end_date = st.sidebar.date_input("End Date", df["day"].max())

df = df[(df["day"] >= pd.to_datetime(start_date)) &
        (df["day"] <= pd.to_datetime(end_date))]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(df))
col2.metric("Anomalies", df["final_anomaly"].sum())
col3.metric("Avg Energy", round(df["total_energy"].mean(), 2))

st.divider()

# Show anomalies
st.subheader("🚨 Detected Anomalies")

st.dataframe(
    df[df["final_anomaly"] == True][
        ["day", "total_energy", "avg_energy", "z_score", "ml_score"]
    ],
    use_container_width=True
)

st.divider()

# Visualization
import plotly.express as px

fig = px.line(df, x="day", y="total_energy", title="Energy Trend")

anoms = df[df["final_anomaly"] == True]

fig.add_scatter(
    x=anoms["day"],
    y=anoms["total_energy"],
    mode="markers",
    name="Anomaly",
    marker=dict(size=10)
)

st.plotly_chart(fig, use_container_width=True)