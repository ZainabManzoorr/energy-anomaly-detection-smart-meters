import pandas as pd
import os


class MultiHouseDataLoader:

    def __init__(self, folder_path: str):
        self.folder_path = folder_path

    def get_files(self):
        return [
            f for f in os.listdir(self.folder_path)
            if f.endswith(".csv")
        ]

    def load_all(self, max_rows_per_file=200000):
        all_data = []

        for file in self.get_files():
            path = os.path.join(self.folder_path, file)

            print(f"Loading: {file}")

            # STREAMING LOAD (CRITICAL FIX)
            df = pd.read_csv(
                path,
                engine="c",
                low_memory=True,
                nrows=max_rows_per_file  # prevents memory crash
            )

            df.columns = [c.lower().strip() for c in df.columns]
            df["house_id"] = file.replace(".csv", "")

            all_data.append(df)

        return pd.concat(all_data, ignore_index=True)