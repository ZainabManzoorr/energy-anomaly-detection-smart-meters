import matplotlib.pyplot as plt


class AnomalyVisualizer:

    def plot_ml_anomalies(self, df, col="aggregate"):

        plt.figure(figsize=(12, 5))

        plt.plot(df[col], label="Energy")

        anomalies = df[df["anomaly"] == 1]

        plt.scatter(
            anomalies.index,
            anomalies[col],
            color="red",
            label="Anomaly"
        )

        plt.title("ML-Based Energy Anomalies")

        plt.legend()

        plt.tight_layout()

        plt.show()

    def plot_appliance_anomalies(self, df, appliance_col):

        plt.figure(figsize=(12, 4))

        plt.plot(df[appliance_col], label=appliance_col)

        anomalies = df[df[f"{appliance_col}_anomaly"] == 1]

        plt.scatter(
            anomalies.index,
            anomalies[appliance_col],
            color="red"
        )

        plt.title(f"Anomalies in {appliance_col}")

        plt.tight_layout()

        plt.show()