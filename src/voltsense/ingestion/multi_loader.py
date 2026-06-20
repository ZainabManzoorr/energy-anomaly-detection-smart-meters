import pandas as pd
from pathlib import Path

class DataLoader:

    def load_data(self, relative_path):
        base_path = Path(__file__).resolve().parents[3]
        file_path = base_path / relative_path

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        df = pd.read_csv(file_path)
        df.columns = [c.lower().strip() for c in df.columns]

        return df
     


    def sample_by_house(
       self,
       df,
       house_sample_size: int = 20):

        sampled_df = (
        df.sort_values(["house_id", "unix"])
          .groupby("house_id", group_keys=False)
          .head(house_sample_size)
          .reset_index(drop=True)
        )

        return sampled_df


    
    """
    Randomly samples up to `house_sample_size`
    rows from each house.

    Used for fast development and EDA.
    Not recommended for sequence modeling
    because temporal order is lost.
    """
