import pandas as pd
import numpy as np

class RuleBasedAnomalyDetector:
    """
    Production-style rule-based anomaly engine for energy monitoring systems
    """

    def __init__(self, df: pd.DataFrame, energy_col: str):
        self.df = df.copy()
        self.energy_col = energy_col

    # --------------------------
    # Z-SCORE ANOMALY DETECTION
    # --------------------------
    def detect_zscore(self, threshold=2):
        mean = self.df[self.energy_col].mean()
        std = self.df[self.energy_col].std()

        if std == 0:
            self.df["z_score"] = 0
            self.df["z_anomaly"] = False
            return self.df

        z = (self.df[self.energy_col] - mean) / std
        self.df["z_score"] = z

        self.df["z_anomaly"] = (z > threshold) | (z < -threshold)

        return self.df

    # --------------------------
    # SPIKE DETECTION
    # --------------------------
    def detect_spikes(self, window=10, multiplier=2):
        rolling_mean = self.df[self.energy_col].rolling(
            window, min_periods=1
        ).mean()

        self.df["rolling_mean"] = rolling_mean

        self.df["spike_anomaly"] = (
            rolling_mean.notna() &
            (self.df[self.energy_col] > rolling_mean * multiplier)
        )

        return self.df

    # --------------------------
    # FINAL COMBINED SIGNAL
    # --------------------------
    def combine_anomalies(self):
        self.df["anomaly"] = (
            self.df.get("z_anomaly", False) |
            self.df.get("spike_anomaly", False)
        )
        return self.df