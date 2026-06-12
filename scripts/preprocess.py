from voltsense.ingestion.multi_loader import MultiHouseDataLoader
from voltsense.analytics.energy_analytics import EnergyAnalytics
import pandas as pd

# -------------------------
# Load raw data
# -------------------------
loader = MultiHouseDataLoader("data/raw/refit_extracted")
df = loader.load_all()

# -------------------------
# Feature engineering
# -------------------------
analytics = EnergyAnalytics(df)
analytics.prepare_time_series()

daily = analytics.daily_consumption()
hourly = analytics.hourly_consumption()
houses = analytics.house_consumption()
weekend = analytics.weekend_vs_weekday()

# -------------------------
# SAVE PROCESSED DATA (IMPORTANT LINE)
# -------------------------
daily.to_csv("data/processed_daily.csv", index=False)
hourly.to_csv("data/processed_hourly.csv", index=False)
houses.to_csv("data/processed_houses.csv", index=False)
weekend.to_csv("data/processed_weekend.csv", index=False)

print("Processed data saved successfully")