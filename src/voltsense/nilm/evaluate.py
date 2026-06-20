import numpy as np
import torch

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


APPLIANCE_NAMES = [
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


def evaluate_nilm(model, X, y):

    model.eval()

    with torch.no_grad():

        preds = model(X)

    preds = preds.cpu().numpy()
    y = y.cpu().numpy()

    print("\n========== NILM EVALUATION ==========\n")

    results = []

    for i, appliance in enumerate(APPLIANCE_NAMES):

        mae = mean_absolute_error(
            y[:, i],
            preds[:, i]
        )

        rmse = np.sqrt(
            mean_squared_error(
                y[:, i],
                preds[:, i]
            )
        )

        r2 = r2_score(
            y[:, i],
            preds[:, i]
        )

        results.append(
            {
                "appliance": appliance,
                "mae": mae,
                "rmse": rmse,
                "r2": r2
            }
        )

        print(
            f"{appliance:<12}"
            f" MAE={mae:.4f}"
            f" RMSE={rmse:.4f}"
            f" R²={r2:.4f}"
        )

    return results, preds