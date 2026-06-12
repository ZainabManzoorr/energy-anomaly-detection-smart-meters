from voltsense.ingestion.multi_loader import MultiHouseDataLoader
from voltsense.analytics.energy_analytics import EnergyAnalytics
from voltsense.anomaly.rule_based import RuleBasedAnomalyDetector
from voltsense.anomaly.ml_based import IsolationForestModel
from voltsense.anomaly.hybrid import HybridAnomalyDetector
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
# Visualizations (basic)
# -------------------------
EnergyPlots.plot_daily_total(daily)
EnergyPlots.plot_daily_average(daily)
EnergyPlots.plot_hourly(hourly)
EnergyPlots.plot_house_comparison(houses)
EnergyPlots.plot_weekend_vs_weekday(weekend)

# -------------------------
# Rule-based anomaly detection
# -------------------------
detector = RuleBasedAnomalyDetector(
    daily,
    energy_col="total_energy"
)

rule_df = detector.detect_zscore(threshold=2)

rule_df = detector.detect_spikes()

# -------------------------
# ML anomaly detection
# -------------------------
ml = IsolationForestModel(
    rule_df,
    features=["total_energy", "avg_energy"]
)

ml_df = ml.run()

# -------------------------
# Hybrid
# -------------------------
hybrid = HybridAnomalyDetector(ml_df)
final_df = hybrid.run()

# -------------------------
# OPTIONAL: anomaly labels
# -------------------------
def create_anomaly_type(df):

    df = df.copy()

    def label(row):
        if row["final_anomaly"]:
            if row["ml_anomaly"] and row["z_anomaly"]:
                return "high"
            elif row["ml_anomaly"]:
                return "ml"
            else:
                return "rule"
        return "normal"

    df["anomaly_type"] = df.apply(label, axis=1)
    return df


final_df = create_anomaly_type(final_df)

# -------------------------
# Visualization (anomalies)
# -------------------------
EnergyPlots.plot_anomalies(final_df)