import matplotlib.pyplot as plt


class EnergyPlots:

    @staticmethod
    def plot_daily_total(daily_df):
        plt.figure(figsize=(12, 5))

        plt.plot(
            daily_df["day"],
            daily_df["total_energy"],
            linewidth=2
        )

        plt.title("Daily Total Energy Consumption")
        plt.xlabel("Date")
        plt.ylabel("Total Energy")

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_daily_average(daily_df):
        plt.figure(figsize=(12, 5))

        plt.plot(
            daily_df["day"],
            daily_df["avg_energy"],
            linewidth=2
        )

        plt.title("Daily Average Energy Consumption")
        plt.xlabel("Date")
        plt.ylabel("Average Energy")

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_hourly(hourly_df):
        plt.figure(figsize=(10, 5))

        plt.plot(
            hourly_df["hour"],
            hourly_df["energy"],
            marker="o",
            linewidth=2
        )

        plt.title("VoltSense — Average Hourly Energy Consumption")
        plt.xlabel("Hour")
        plt.ylabel("Average Energy")
        plt.xticks(range(24))
        plt.grid(alpha=0.3)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_house_comparison(houses_df):
        plt.figure(figsize=(10, 6))

        plt.barh(
            houses_df["house_id"],
            houses_df["total_energy"]
        )

        plt.gca().invert_yaxis()

        plt.title("VoltSense — Total Energy Consumption by House")
        plt.xlabel("Total Energy")
        plt.ylabel("House")

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_weekend_vs_weekday(weekend_df):

        labels = [
            "Weekday" if not x else "Weekend"
            for x in weekend_df["is_weekend"]
        ]

        plt.figure(figsize=(6, 5))

        plt.bar(
            labels,
            weekend_df["avg_energy"]
        )

        plt.title("Average Energy: Weekday vs Weekend")
        plt.xlabel("Day Type")
        plt.ylabel("Average Energy")

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_anomalies(result_df):

        plt.figure(figsize=(14, 5))

        plt.plot(
            result_df["day"],
            result_df["total_energy"],
            label="Daily Energy",
            linewidth=2
        )

        high = result_df[
            result_df["anomaly_type"] == "high"
        ]

        low = result_df[
            result_df["anomaly_type"] == "low"
        ]

        plt.scatter(
            high["day"],
            high["total_energy"],
            s=70,
            label="High Anomaly"
        )

        plt.scatter(
            low["day"],
            low["total_energy"],
            s=70,
            label="Low Anomaly"
        )

        plt.title("VoltSense — Daily Energy Anomalies")
        plt.xlabel("Date")
        plt.ylabel("Total Energy")

        plt.legend()

        plt.tight_layout()
        plt.show()