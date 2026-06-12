import matplotlib.pyplot as plt
from pathlib import Path
import os


class EnergyPlots:

    
    OUTPUT_DIR = Path.cwd() / "outputs" / "plots"

    @staticmethod
    def _save(fig_name):

        # Ensure folder exists
        EnergyPlots.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        path = EnergyPlots.OUTPUT_DIR / fig_name

        # Save figure
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()

        print(f"✅ Saved: {path.resolve()}")

    # -------------------------
    # 1. DAILY ENERGY
    # -------------------------
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

        EnergyPlots._save("daily_total_energy.png")
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

        EnergyPlots._save("daily_average_energy.png")

    # -------------------------
    # 2. HOURLY PATTERN
    # -------------------------
    @staticmethod
    def plot_hourly(hourly_df):

        plt.figure(figsize=(10, 5))

        plt.plot(
            hourly_df["hour"],
            hourly_df["energy"],
            marker="o",
            linewidth=2
        )

        plt.title("Hourly Energy Consumption")
        plt.xlabel("Hour")
        plt.ylabel("Energy")
        plt.xticks(range(24))
        plt.grid(alpha=0.3)

        EnergyPlots._save("hourly_energy_pattern.png")

    # -------------------------
    # 3. HOUSE COMPARISON
    # -------------------------
    @staticmethod
    def plot_house_comparison(houses_df):

        plt.figure(figsize=(10, 6))

        plt.barh(
            houses_df["house_id"],
            houses_df["total_energy"]
        )

        plt.gca().invert_yaxis()

        plt.title("House Energy Comparison")
        plt.xlabel("Total Energy")
        plt.ylabel("House ID")

        EnergyPlots._save("house_comparison.png")

    # -------------------------
    # 4. WEEKEND VS WEEKDAY
    # -------------------------
    @staticmethod
    def plot_weekend_vs_weekday(weekend_df):

        labels = [
            "Weekend" if x else "Weekday"
            for x in weekend_df["is_weekend"]
        ]

        plt.figure(figsize=(6, 5))

        plt.bar(labels, weekend_df["avg_energy"])

        plt.title("Weekend vs Weekday Energy Usage")
        plt.xlabel("Day Type")
        plt.ylabel("Average Energy")

        EnergyPlots._save("weekend_vs_weekday.png")

    # -------------------------
    # 5. ANOMALIES
    # -------------------------
    @staticmethod
    def plot_anomalies(result_df):

        plt.figure(figsize=(14, 5))

        plt.plot(
            result_df["day"],
            result_df["total_energy"],
            linewidth=2,
            label="Energy"
        )

        high = result_df[result_df["anomaly_type"] == "high"]
        low = result_df[result_df["anomaly_type"] == "low"]

        plt.scatter(high["day"], high["total_energy"], label="High Anomaly", s=70)
        plt.scatter(low["day"], low["total_energy"], label="Low Anomaly", s=70)

        plt.title("Energy Anomalies")
        plt.xlabel("Date")
        plt.ylabel("Energy")

        plt.legend()
        

        EnergyPlots._save("daily_anomalies.png")