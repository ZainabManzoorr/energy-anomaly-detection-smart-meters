import pandas as pd


class DataCleaner:
    """
    Cleans and validates NILM energy data.
    """

    REQUIRED_COLUMNS = [
        "unix",
        "aggregate",
        "house_id"
    ]

    def validate(self, df: pd.DataFrame) -> None:
        """
        Validate required columns exist.
        """

        missing = [
            col
            for col in self.REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Basic cleaning pipeline.
        """

        # Validate schema first
        self.validate(df)

        df = df.copy()

        # Remove missing values
        df = df.dropna()

        # Convert unix timestamp to datetime
        df["datetime"] = pd.to_datetime(
            df["unix"],
            unit="s"
        )

        # Sort by house and time
        df = df.sort_values(
            ["house_id", "unix"]
        )

        # Reset index
        df = df.reset_index(drop=True)

        return df


if __name__ == "__main__":

    from voltsense.ingestion.multi_loader import DataLoader

    loader = DataLoader()

    df = loader.load_data(
        "data/raw/combined_refit.csv"
    )

    cleaner = DataCleaner()

    clean_df = cleaner.clean(df)

    print("Data cleaned successfully")
    print(f"Shape: {clean_df.shape}")

    print("\nColumns:")
    print(clean_df.columns.tolist())

    print("\nFirst 5 rows:")
    print(clean_df.head())