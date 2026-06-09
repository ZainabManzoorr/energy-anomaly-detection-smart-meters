class InsightGenerator:

    @staticmethod
    def peak_hour(hourly_df):

        print("DEBUG columns:", hourly_df.columns)

        # find correct energy column dynamically
        possible_cols = ["avg_energy", "aggregate", "energy"]

        value_col = None
        for col in possible_cols:
            if col in hourly_df.columns:
                value_col = col
                break

        if value_col is None:
            raise ValueError(f"No valid energy column found. Columns are: {list(hourly_df.columns)}")

        peak_row = hourly_df.loc[
            hourly_df[value_col].idxmax()
        ]

        return (
            f"Peak energy usage occurs at "
            f"{int(peak_row['hour'])}:00 with average consumption "
            f"of {peak_row[value_col]:.2f} watts."
        )