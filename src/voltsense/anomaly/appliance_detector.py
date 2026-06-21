from .ml_detector import EnergyMLAnomalyDetector


class ApplianceAnomalyDetector:

    def __init__(self):

        self.detectors = {}

    def fit(self, df, appliance_cols):

        self.appliance_cols = appliance_cols

        for col in appliance_cols:

            print(f"Training anomaly model for {col}")

            model = EnergyMLAnomalyDetector(
                contamination=0.01
            )

            model.fit(
                df,
                feature_cols=[col]
            )

            self.detectors[col] = model

        return self

    def predict(self, df):

        df = df.copy()

        for col, model in self.detectors.items():

            result = model.predict(df)

            df[f"{col}_anomaly"] = result["anomaly"]

        return df