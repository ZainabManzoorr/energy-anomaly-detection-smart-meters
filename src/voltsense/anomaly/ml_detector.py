from sklearn.ensemble import IsolationForest


class EnergyMLAnomalyDetector:

    def __init__(self, contamination=0.01):

        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42
        )

        self.feature_cols = None

    # -------------------------
    # TRAIN MODEL
    # -------------------------
    def fit(self, df, feature_cols):

        self.feature_cols = feature_cols

        X = df[feature_cols]

        self.model.fit(X)

        return self

    # -------------------------
    # PREDICT ANOMALIES
    # -------------------------
    def predict(self, df):

        X = df[self.feature_cols]

        df = df.copy()

        df["anomaly_score"] = self.model.decision_function(X)

        df["anomaly"] = self.model.predict(X)

        # convert sklearn output
        df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})

        return df