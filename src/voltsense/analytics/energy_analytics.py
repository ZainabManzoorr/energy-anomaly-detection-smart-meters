import pandas as pd


class EnergyAnalytics:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # -------------------------
    # TIME FEATURE ENGINEERING
    # -------------------------
    def prepare_time_series(self):

        self.df["time"] = pd.to_datetime(self.df["time"])
        self.df = self.df.sort_values("time")

        self.df["hour"] = self.df["time"].dt.hour
        self.df["day"] = self.df["time"].dt.date.astype(str)  # stable for grouping
        self.df["weekday"] = self.df["time"].dt.day_name()
        self.df["month"] = self.df["time"].dt.month

        self.df["is_weekend"] = self.df["weekday"].isin(
            ["Saturday", "Sunday"]
        )

        return self.df

    # -------------------------
    # DAILY ENERGY
    # -------------------------
    def daily_consumption(self):

        return (
            self.df.groupby("day", as_index=False)
            .agg(
                total_energy=("aggregate", "sum"),
                avg_energy=("aggregate", "mean")
            )
        )

    # -------------------------
    # HOURLY ENERGY
    # -------------------------
    def hourly_consumption(self):

        return (
            self.df.groupby("hour", as_index=False)
            .agg(energy=("aggregate", "mean"))
        )

    # -------------------------
    # HOUSE COMPARISON
    # -------------------------
    def house_consumption(self):

        return (
            self.df.groupby("house_id", as_index=False)
            .agg(total_energy=("aggregate", "sum"))
            .sort_values("total_energy", ascending=False)
        )

    # -------------------------
    # WEEKEND ANALYSIS
    # -------------------------
    def weekend_vs_weekday(self):

        return (
            self.df.groupby("is_weekend", as_index=False)
            .agg(avg_energy=("aggregate", "mean"))
        )