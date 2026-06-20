import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from src.voltsense.models.lstm import EnergyLSTM


def train_model(train_dataset):

    train_loader = DataLoader(
        train_dataset,
        batch_size=64,
        shuffle=False
    )

    model = EnergyLSTM(
        input_size=9
    )

    criterion = nn.MSELoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.001
    )

    epochs = 5

    for epoch in range(epochs):

        model.train()

        running_loss = 0

        for X_batch, y_batch in train_loader:

            predictions = model(X_batch)

            loss = criterion(
                predictions,
                y_batch
            )

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            running_loss += loss.item()

        print(
            f"Epoch {epoch+1} | Loss: {running_loss:.4f}"
        )

    return model