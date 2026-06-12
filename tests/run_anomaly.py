from voltsense.ingestion.multi_loader import MultiHouseDataLoader
from voltsense.analytics.energy_analytics import EnergyAnalytics
from voltsense.anomaly.rule_based import RuleBasedAnomalyDetector
from voltsense.anomaly.ml_based import IsolationForestModel
from voltsense.anomaly.hybrid import HybridAnomalyDetector

# Load Data
loader = MultiHouseDataLoader("data/raw/refit_extracted")
df = loader.load_all()

# Analytics
analytics = EnergyAnalytics(df)

df = analytics.prepare_time_series()

daily = analytics.daily_consumption()

# Rule-Based Detection
detector = RuleBasedAnomalyDetector(
    daily,
    energy_col="total_energy"
)

rule_result = detector.detect_zscore()

detector = RuleBasedAnomalyDetector(
    rule_result,
    energy_col="total_energy"
)

rule_result = detector.detect_spikes()

# -----------------------------
# ML DETECTOR
# -----------------------------
ml = IsolationForestModel(
    rule_result,
    features=["total_energy", "avg_energy"]
)

ml_result = ml.run()

# -----------------------------
# HYBRID ENGINE
# -----------------------------
hybrid = HybridAnomalyDetector(ml_result)
final_df = hybrid.run()

# -----------------------------
# ADD THIS (IMPORTANT)
# -----------------------------
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