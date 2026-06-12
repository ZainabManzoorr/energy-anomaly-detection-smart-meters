import pandas as pd

class FeatureScaler:

    @staticmethod
    def normalize_energy(df, col):
        df = df.copy()
        df[f"{col}_norm"] = df[col] / df[col].max()
        return df