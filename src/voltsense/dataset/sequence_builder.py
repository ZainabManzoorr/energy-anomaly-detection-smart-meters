import numpy as np
import pandas as pd


class SequenceBuilder:
    """
    Converts tabular time-series into ML sequences for LSTM/GRU.

    Goal:
    X = past N timesteps
    y = next timestep (or appliance prediction)
    """

    def __init__(self, sequence_length=30):
        self.sequence_length = sequence_length

    def scale(self, df):
        """
        Scale ONLY continuous energy features.
        """

        df = df.copy()

        self.scalers = {}

        cols_to_scale = [
            "aggregate",
            "total_appliance_usage",
            "residual_load"
        ]

        for col in cols_to_scale:
            max_val = df[col].max()
            self.scalers[col] = max_val

            df[col] = df[col] / (max_val + 1e-8)

        return df

    def create_sequences(self, df, target_col="aggregate"):
        """
        Converts dataframe into LSTM-ready format.

        Returns:
        X: (samples, timesteps, features)
        y: (samples,)
        """

        df = df.sort_values(["house_id", "unix"]).reset_index(drop=True)

        feature_cols = [
            "aggregate",
            "total_appliance_usage",
            "residual_load",
            "hour",
            "weekday",
            "is_night",
            "is_weekend",
            "agg_lag_1",
            "agg_lag_2",
        ]

        X, y = [], []

        for i in range(len(df) - self.sequence_length):
            seq_x = df.iloc[i:i+self.sequence_length][feature_cols].values
            seq_y = df.iloc[i+self.sequence_length][target_col]

            X.append(seq_x)
            y.append(seq_y)

        return np.array(X), np.array(y)
      
print(f"Sequenced dataset")