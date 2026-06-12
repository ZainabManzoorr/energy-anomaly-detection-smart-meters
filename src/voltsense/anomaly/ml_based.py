from sklearn.ensemble import IsolationForest

class IsolationForestModel:

    def __init__(self, df, features):
        self.df = df.copy()
        self.features = features

        self.model = IsolationForest(
            n_estimators=200,
            contamination="auto",
            random_state=42,
            n_jobs=-1
        )

    def run(self):

        X = self.df[self.features].fillna(0)

        self.model.fit(X)

        self.df["ml_anomaly"] = (
            self.model.predict(X) == -1
        )

        self.df["ml_score"] = self.model.decision_function(X)

        return self.df