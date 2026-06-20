# src/voltsense/nilm/dataset_builder.py

import numpy as np


class NILMSequenceBuilder:

    def __init__(self, sequence_length=30):
        self.sequence_length = sequence_length

    def create(self, df):

        feature_cols = [
            "aggregate",
            "hour",
            "weekday",
            "is_night",
            "is_weekend",
            "agg_lag_1",
            "agg_lag_2",
        ]

        target_cols = [
            "appliance1",
            "appliance2",
            "appliance3",
            "appliance4",
            "appliance5",
            "appliance6",
            "appliance7",
            "appliance8",
            "appliance9",
        ]

        X, y = [], []

        for house_id, house_df in df.groupby("house_id"):

            house_df = house_df.sort_values("unix")

            X_data = house_df[feature_cols].to_numpy()
            y_data = house_df[target_cols].to_numpy()

            for i in range(len(house_df) - self.sequence_length):

                X.append(
                    X_data[i:i+self.sequence_length]
                )

                y.append(
                    y_data[i+self.sequence_length]
                )

        return np.array(X), np.array(y)