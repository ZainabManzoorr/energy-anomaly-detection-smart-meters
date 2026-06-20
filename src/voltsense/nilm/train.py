import torch
import torch.nn as nn
from torch.utils.data import DataLoader


class WeightedMSELoss(nn.Module):
    """
    Fixes appliance imbalance problem.
    """

    def __init__(self, weights=None):

        super().__init__()

        if weights is None:
            # default balanced weights for 9 appliances
            weights = torch.tensor([
                1.5,  # small appliance (lights)
                1.5,
                1.0,
                1.0,
                2.0,  # rare appliance
                1.0,
                1.2,
                1.0,
                1.0,
            ])

        self.weights = weights

    def forward(self, pred, target):

        loss = (pred - target) ** 2
        loss = loss * self.weights

        return loss.mean()


def train_nilm(model, dataset):

    loader = DataLoader(
        dataset,
        batch_size=64,
        shuffle=True
    )

    # ✅ FIX 1: better loss
    criterion = WeightedMSELoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.001
    )

    for epoch in range(5):

        model.train()

        total_loss = 0

        for X, y in loader:

            preds = model(X)

            loss = criterion(preds, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(loader)

        print(f"Epoch {epoch+1} | Avg Loss: {avg_loss:.6f}")

    return model