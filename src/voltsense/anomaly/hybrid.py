class HybridAnomalyDetector:

    def __init__(self, df):
        self.df = df.copy()

    def run(self):

        # Count how many detectors flagged the point
        self.df["anomaly_votes"] = (
            self.df["z_anomaly"].astype(int)
            + self.df["spike_anomaly"].astype(int)
            + self.df["ml_anomaly"].astype(int)
        )

        # Majority voting (2 out of 3)
        self.df["final_anomaly"] = (
            self.df["anomaly_votes"] >= 2
        )

        return self.df