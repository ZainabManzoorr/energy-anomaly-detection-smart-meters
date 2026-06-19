import pandas as pd


class FeatureEngineer:
    """
    Feature engineering for NILM (Non-Intrusive Load Monitoring)

    Goal:
    Convert raw energy + timestamp data into behavioral + temporal signals
    that ML models can learn from.
    """

    def __init__(self):
        self.appliance_cols = None

    def fit(self, df: pd.DataFrame):
        """
        Identify appliance columns dynamically
        (appliance1, appliance2, ..., applianceN)
        """
        self.appliance_cols = [
            col for col in df.columns
            if "appliance" in col
        ]
        return self

    # -----------------------------
    # TIME-BASED FEATURES
    # -----------------------------

    def add_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # Hour of day (0–23)
        # Helps model learn daily usage cycles:
        # e.g., cooking in evening, low usage at night
        df["hour"] = df["datetime"].dt.hour

        # Day of week (0=Monday, 6=Sunday)
        # Captures weekday vs weekend behavior differences
        df["weekday"] = df["datetime"].dt.weekday

        # Day of month
        # Captures long-term monthly patterns (weak but useful for trends)
        df["day"] = df["datetime"].dt.day

        # Night indicator (1 if late night or early morning)
        # Helps model learn base load vs human activity periods
        df["is_night"] = (
            (df["hour"] >= 22) | (df["hour"] <= 6)
        ).astype(int)

        # Weekend indicator
        # Captures behavioral shift: more appliance usage at home
        df["is_weekend"] = (
            df["weekday"] >= 5
        ).astype(int)

        return df

    # -----------------------------
    # ENERGY STRUCTURE FEATURES
    # -----------------------------

    def add_energy_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if self.appliance_cols is None:
            self.fit(df)

        # Total appliance consumption at each timestamp
        # Helps validate dataset consistency:
        # aggregate ≈ sum(appliances)
        df["total_appliance_usage"] = df[self.appliance_cols].sum(axis=1)

        # Residual load = unexplained energy
        # VERY IMPORTANT for NILM:
        # captures unknown appliances + noise + measurement error
        df["residual_load"] = df["aggregate"] - df["total_appliance_usage"]

        return df

    # -----------------------------
    # TEMPORAL / STATISTICAL FEATURES
    # -----------------------------

    def add_statistical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # Rolling mean (window=5)
        # Captures short-term energy trend (smooth usage behavior)
        df["agg_roll_mean_5"] = df["aggregate"].rolling(5).mean()

        # Rolling standard deviation
        # Captures volatility in energy usage
        # High std = sudden appliance activity (kettle, microwave, etc.)
        df["agg_roll_std_5"] = df["aggregate"].rolling(5).std()

        # Lag feature (previous timestep)
        # Gives model short-term memory
        # Helps predict current usage based on previous state
        df["agg_lag_1"] = df["aggregate"].shift(1)

        # Lag feature (2 steps back)
        # Captures short sequence patterns
        # Useful for temporal models like LSTM/GRU
        df["agg_lag_2"] = df["aggregate"].shift(2)

        return df

    # -----------------------------
    # FULL PIPELINE
    # -----------------------------

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies full feature engineering pipeline:

        1. Time-based features
        2. Energy structure features
        3. Temporal/statistical features
        """

        df = df.copy()

        df = self.add_time_features(df)
        df = self.add_energy_features(df)
        df = self.add_statistical_features(df)

        # Remove NaNs created by rolling + lag operations
        # Important because ML models cannot handle missing values
        df = df.dropna().reset_index(drop=True)

        return df

print(f"Feature engineering done")