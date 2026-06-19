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
     
    def sample_by_house(self, df, house_sample_size: int, random_state: int = 42):

        sampled_df = (
            df.groupby("house_id", group_keys=False)
              .apply(lambda x: x.sample(
                  n=min(len(x), house_sample_size),
                  random_state=random_state
              ))
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
    print(f"data loaded")