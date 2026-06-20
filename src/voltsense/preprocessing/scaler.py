import pandas as pd

class Scaler:

    def fit(self, df):
        self.max_vals = {}

        for col in ["aggregate", "total_appliance_usage", "residual_load"]:
            self.max_vals[col] = df[col].max()

    def transform(self, df):
        df = df.copy()

        for col, max_val in self.max_vals.items():
            df[col] = df[col] / (max_val + 1e-8)

        return df
      
