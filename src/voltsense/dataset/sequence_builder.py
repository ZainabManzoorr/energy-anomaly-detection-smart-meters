import numpy as np


class SequenceBuilder:

    def __init__(self, sequence_length=30):
        self.sequence_length = sequence_length

    def create_sequences(self, df, target_col="aggregate"):

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

        X = []
        y = []

        for house_id, house_df in df.groupby("house_id"):

            print(f"Processing {house_id}...")

            house_df = house_df.sort_values("unix")

            features = house_df[feature_cols].to_numpy()
            target = house_df[target_col].to_numpy()

            for i in range(len(house_df) - self.sequence_length):

                X.append(
                    features[i:i+self.sequence_length]
                )

                y.append(
                    target[i+self.sequence_length]
                )

        X = np.array(X, dtype=np.float32)
        y = np.array(y, dtype=np.float32)

        print("Sequences created")
        print("X shape:", X.shape)
        print("y shape:", y.shape)

        return X, y