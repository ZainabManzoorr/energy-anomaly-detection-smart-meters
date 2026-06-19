from src.voltsense.ingestion.multi_loader import DataLoader
from src.voltsense.cleaning.clean import DataCleaner
from src.voltsense.features.feature import FeatureEngineer
from src.voltsense.preprocessing.scaler import Scaler
from src.voltsense.dataset.sequence_builder import SequenceBuilder


def run_pipeline():

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
    # SAMPLING 
    # -------------------------
    df = df.groupby("house_id").head(100000).reset_index(drop=True)

    print("Sampled data:", df.shape)

    # -------------------------
    # 3. FEATURE ENGINEERING
    # -------------------------
    fe = FeatureEngineer()
    df = fe.transform(df)

    print("Features created:", df.shape)

    # -------------------------
    # 4. SCALING (FIXED FLOW)
    # -------------------------
    scaler = Scaler()

    scaler.fit(df)
    df = scaler.transform(df)

    print("Scaling done")

    # -------------------------
    # 5. SEQUENCE BUILDING
    # -------------------------
    builder = SequenceBuilder(sequence_length=30)

    X, y = builder.create_sequences(df)

    print("Sequences created")
    print("X shape:", X.shape)
    print("y shape:", y.shape)

    return X, y


if __name__ == "__main__":
    X, y = run_pipeline()