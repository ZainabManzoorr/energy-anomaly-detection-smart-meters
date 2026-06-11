import pandas as pd


class EnergyAnalytics:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    
    # TIME FEATURE ENGINEERING
    
    def prepare_time_series(self):
        self.df["time"] = pd.to_datetime(self.df["time"])

        self.df = self.df.sort_values("time")

        self.df["hour"] = self.df["time"].dt.hour
        self.df["day"] = self.df["time"].dt.date
        self.df["weekday"] = self.df["time"].dt.day_name()
        self.df["month"] = self.df["time"].dt.month
        self.df["is_weekend"] = self.df["weekday"].isin(
            ["Saturday", "Sunday"]
        )

        return self.df

    
    # DAILY ENERGY
    
    def daily_consumption(self):
        return (
            self.df.groupby("day", as_index=False).agg(
            total_energy=("aggregate", "sum"),
            avg_energy=("aggregate", "mean")
            ).reset_index()
        )

    
    # HOURLY ENERGY PATTERN
    
    def hourly_consumption(self):
        return (
            self.df.groupby("hour", as_index=False)["aggregate"]
            .mean()
            .rename(columns={"aggregate": "energy"})
        )

   
    # HOUSE COMPARISON
    
    def house_consumption(self):
     return (
        self.df.groupby("house_id")["aggregate"]
        .sum()
        .reset_index()
        .rename(columns={"aggregate": "total_energy"})
        .sort_values("total_energy", ascending=False)
    )

    
    # WEEKDAY vs WEEKEND
    
    def weekend_vs_weekday(self):
     return (
        self.df.groupby("is_weekend")["aggregate"]
        .mean()
        .reset_index()
        .rename(columns={"aggregate": "avg_energy"})
    )