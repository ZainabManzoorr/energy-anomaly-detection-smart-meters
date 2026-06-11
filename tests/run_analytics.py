from voltsense.ingestion.multi_loader import MultiHouseDataLoader
from voltsense.analytics.energy_analytics import EnergyAnalytics
from voltsense.insight.insight_generator import InsightGenerator

# -----------------------------
# LOAD DATA
# -----------------------------
loader = MultiHouseDataLoader("data/raw/refit_extracted")
df = loader.load_all()

analytics = EnergyAnalytics(df)
base_df = analytics.prepare_time_series()

hourly = analytics.hourly_consumption()
daily = analytics.daily_consumption()
houses = analytics.house_consumption()
weekend_stats = analytics.weekend_vs_weekday()

detector = RuleBasedAnomalyDetector(daily, energy_col="consumption")
high_anomalies, low_anomalies = detector.detect_daily_spikes()

insights = InsightGenerator()

print(insights.peak_hour(hourly))
print(insights.lowest_hour(hourly))
print(insights.highest_consuming_house(houses))
print(insights.weekend_summary(weekend_stats))
print(insights.anomaly_summary(high_anomalies, low_anomalies))
RuleBasedAnomalyDetector.detect_daily_spikes(daily)


print("\nHigh Energy Anomalies")
print(high_anomalies)
print("\nLow Energy Anomalies")
print(low_anomalies)
# -----------------------------
# INSIGHTS
# -----------------------------
print("\nINSIGHT:")
print(InsightGenerator.peak_hour(hourly))
print(InsightGenerator.lowest_hour(hourly))
print(InsightGenerator.highest_consuming_house(houses))
print(InsightGenerator.weekend_summary(weekend_stats))
print(InsightGenerator.anomaly_summary(high_anomalies, low_anomalies))

