from voltsense.ingestion.multi_loader import MultiHouseDataLoader
from voltsense.analytics.energy_analytics import EnergyAnalytics
from voltsense.anomaly.rule_based import RuleBasedAnomalyDetector
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

# -----------------------------
# RULE-BASED ANOMALY DETECTION
# -----------------------------
detector = RuleBasedAnomalyDetector(
    daily,
    energy_col="total_energy"
)

high_anomalies, low_anomalies = detector.detect_daily_spikes()

# -----------------------------
# INSIGHT GENERATOR (INSTANCE STYLE)
# -----------------------------
insights = InsightGenerator()

print("\n--- ENERGY INSIGHTS ---")

print(insights.peak_hour(hourly))
print(insights.lowest_hour(hourly))
print(insights.highest_consuming_house(houses))
print(insights.weekend_summary(weekend_stats))
print(insights.anomaly_summary(high_anomalies, low_anomalies))