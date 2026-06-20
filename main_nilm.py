from src.voltsense.ingestion.multi_loader import DataLoader
from src.voltsense.cleaning.clean import DataCleaner
from src.voltsense.features.feature import FeatureEngineer
from src.voltsense.preprocessing.scaler import Scaler

from src.voltsense.nilm.dataset_builder import NILMSequenceBuilder
from src.voltsense.nilm.model import NILMLSTM
from src.voltsense.nilm.train import train_nilm
from src.voltsense.nilm.scaler import TargetScaler

from src.voltsense.nilm.evaluate import evaluate_nilm
from src.voltsense.nilm.visualize import plot_predictions

import torch
from torch.utils.data import TensorDataset
import os


def run_nilm_pipeline():

    # -------------------------
    # 1. LOAD DATA
    # -------------------------
    loader = DataLoader()
    df = loader.load_data("data/raw/combined_refit.csv")

    print("Data loaded:", df.shape)

    # -------------------------
    # 2. CLEAN DATA
    # -------------------------
    cleaner = DataCleaner()
    df = cleaner.clean(df)

    print("Data cleaned:", df.shape)

    # -------------------------
    # 3. SAMPLING
    # -------------------------
    df = loader.sample_by_house(df, house_sample_size=5000)

    print("Sampled data:", df.shape)

    # -------------------------
    # 4. FEATURE ENGINEERING
    # -------------------------
    fe = FeatureEngineer()
    df = fe.transform(df)

    print("Features created:", df.shape)

    # -------------------------
    # 5. SCALING
    # -------------------------
    scaler = Scaler()
    scaler.fit(df)
    df = scaler.transform(df)

    print("Scaling done")

    # -------------------------
    # 6. SEQUENCE BUILDING
    # -------------------------
    builder = NILMSequenceBuilder(sequence_length=30)
    X, y = builder.create(df)

    print("NILM sequences created")
    print("X shape:", X.shape)
    print("y shape:", y.shape)
    
    target_scaler = TargetScaler()
    target_scaler.fit(y)
    y = target_scaler.transform(y)

    # -------------------------
    # 7. TO TENSORS
    # -------------------------
    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32)

    dataset = TensorDataset(X, y)

    # -------------------------
    # 8. MODEL
    # -------------------------
    input_size = X.shape[2]
    model = NILMLSTM(input_size=input_size)

    # -------------------------
    # 9. TRAIN
    # -------------------------
    trained_model = train_nilm(model, dataset)
    results, preds = evaluate_nilm(
    trained_model,
    X,
    y
    )
    plot_predictions(
    actual=y[:, 0].cpu().numpy(),
    predicted=preds[:, 0],
    appliance_name="Appliance 1"
    )

    # -------------------------
    # 10. SAVE MODEL
    # -------------------------
    os.makedirs("models", exist_ok=True)

    torch.save(
        trained_model.state_dict(),
        "models/nilm_model.pt"
    )

    print("NILM model trained and saved")

    return trained_model


if __name__ == "__main__":
    run_nilm_pipeline()