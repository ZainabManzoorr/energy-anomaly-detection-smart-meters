import numpy as np

class TargetScaler:

    def fit(self, y):
        self.max_vals = np.max(y, axis=0)

    def transform(self, y):
        return y / (self.max_vals + 1e-8)

    def inverse_transform(self, y):
        return y * self.max_vals