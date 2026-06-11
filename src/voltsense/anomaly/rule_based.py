import pandas as pd

class RuleBasedAnomalyDetector:
    """
    Production-style rule-based anomaly engine for VoltSense
    """

    def __init__(self, df: pd.DataFrame, energy_col: str):
        self.df = df.copy()
        self.energy_col = energy_col

    # --------------------------
    # CORE RULE: Z-SCORE
    # --------------------------
    def detect_zscore(self, threshold=2):
        mean = self.df[self.energy_col].mean()
        std = self.df[self.energy_col].std()

        upper = mean + threshold * std
        lower = mean - threshold * std

        self.df["anomaly_type"] = "normal"

        self.df.loc[self.df[self.energy_col] > upper, "anomaly_type"] = "high"
        self.df.loc[self.df[self.energy_col] < lower, "anomaly_type"] = "low"

        return self.df

    # --------------------------
    # SIMPLE SPIKE RULE
    # --------------------------
    def detect_spikes(self, window=10, multiplier=2):
        rolling_mean = self.df[self.energy_col].rolling(window).mean()

        self.df["rolling_mean"] = rolling_mean

        self.df["spike_anomaly"] = (
            self.df[self.energy_col] > rolling_mean * multiplier
        )

        return self.df