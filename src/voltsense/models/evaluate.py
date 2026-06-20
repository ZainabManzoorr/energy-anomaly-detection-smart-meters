import torch
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


def evaluate(
    model,
    val_loader
):

    model.eval()

    preds = []
    targets = []

    with torch.no_grad():

        for X_batch, y_batch in val_loader:

            output = model(X_batch)

            preds.extend(
                output.squeeze().tolist()
            )

            targets.extend(
                y_batch.squeeze().tolist()
            )

    mae = mean_absolute_error(
        targets,
        preds
    )

    rmse = mean_squared_error(
        targets,
        preds
    ) ** 0.5

    print(f"MAE : {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")