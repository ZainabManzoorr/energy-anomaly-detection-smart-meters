import pandas as pd

pd.options.mode.chained_assignment = None

from voltsense.ingestion.multi_loader import MultiHouseDataLoader

folder_path = "data/raw/refit_extracted"

loader = MultiHouseDataLoader(folder_path)

df = loader.load_all()

df.to_csv("data/processed/combined_refit.csv", index=False)
print("Saved processed dataset successfully.")