from voltsense.ingestion.multi_loader import MultiHouseDataLoader
from voltsense.analytics.energy_analytics import EnergyAnalytics
from voltsense.anomaly.rule_based import RuleBasedAnomalyDetector
from voltsense.visualization.energy_plots import EnergyPlots

# -------------------------
# Load Data
# -------------------------

loader = MultiHouseDataLoader("data/raw/refit_extracted")

df = loader.load_all()

analytics = EnergyAnalytics(df)
analytics.prepare_time_series()

# -------------------------
# Analytics
# -------------------------

daily = analytics.daily_consumption()
hourly = analytics.hourly_consumption()
houses = analytics.house_consumption()
weekend = analytics.weekend_vs_weekday()

# -------------------------
# Visualizations
# -------------------------

EnergyPlots.plot_daily_total(daily)

EnergyPlots.plot_daily_average(daily)

EnergyPlots.plot_hourly(hourly)

EnergyPlots.plot_house_comparison(houses)

EnergyPlots.plot_weekend_vs_weekday(weekend)

# -------------------------
# Anomaly Detection
# -------------------------

detector = RuleBasedAnomalyDetector(
    daily,
    energy_col="total_energy"
)

result = detector.detect_zscore(threshold=2)

EnergyPlots.plot_anomalies(result)