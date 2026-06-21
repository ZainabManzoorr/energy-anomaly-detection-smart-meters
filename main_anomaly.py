from src.voltsense.ingestion.multi_loader import DataLoader
from src.voltsense.cleaning.clean import DataCleaner
from src.voltsense.features.feature import FeatureEngineer

from src.voltsense.anomaly.ml_detector import EnergyMLAnomalyDetector
from src.voltsense.anomaly.appliance_detector import ApplianceAnomalyDetector
from src.voltsense.anomaly.visulize import AnomalyVisualizer


def run_anomaly_pipeline():

    # -------------------------
    # 1. LOAD DATA
    # -------------------------
    loader = DataLoader()
    df = loader.load_data("data/raw/combined_refit.csv")

    print("Data loaded:", df.shape)

    # -------------------------
    # 2. CLEAN DATA
    # -------------------------
    cleaner = DataCleaner()
    df = cleaner.clean(df)

    print("Data cleaned:", df.shape)

    # -------------------------
    # 3. FEATURE ENGINEERING
    # -------------------------
    fe = FeatureEngineer()
    df = fe.transform(df)

    print("Features created:", df.shape)

    # -------------------------
    # 4. ML ANOMALY DETECTION (AGGREGATE)
    # -------------------------
    print("\nTraining aggregate anomaly model...")

    feature_cols = [
        "appliance1",
        "hour",
        "weekday",
        "aggregate"
    ]

    ml_detector = EnergyMLAnomalyDetector(contamination=0.01)

    ml_detector.fit(
        df,
        feature_cols=feature_cols
    )

    df = ml_detector.predict(df)

    print("Aggregate anomaly detection done")

    # -------------------------
    # 5. APPLIANCE-LEVEL ANOMALY DETECTION
    # -------------------------
    print("\nTraining appliance-level anomaly models...")

    appliance_cols = [
        "appliance1",
        "appliance2",
        "appliance3",
        "appliance4",
        "appliance5",
        "appliance6",
        "appliance7",
        "appliance8",
        "appliance9",
    ]

    appliance_detector = ApplianceAnomalyDetector()

    appliance_detector.fit(df, appliance_cols)

    df = appliance_detector.predict(df)

    print("Appliance anomaly detection done")

    # -------------------------
    # 6. VISUALIZATION
    # -------------------------
    print("\nGenerating visualizations...")

    viz = AnomalyVisualizer()

    viz.plot_ml_anomalies(df, col="aggregate")

    viz.plot_appliance_anomalies(df, "appliance1")

    print("\nAnomaly pipeline completed successfully")


if __name__ == "__main__":
    run_anomaly_pipeline()