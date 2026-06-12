class InsightGenerator:

    @staticmethod
    def peak_hour(hourly_df):
        peak = hourly_df.loc[hourly_df["energy"].idxmax()]
        return (
            f"Peak energy usage occurs at {int(peak['hour'])}:00 "
            f"with an average consumption of {peak['energy']:.2f} W."
        )

    @staticmethod
    def lowest_hour(hourly_df):
        low = hourly_df.loc[hourly_df["energy"].idxmin()]
        return (
            f"Lowest energy usage occurs at {int(low['hour'])}:00 "
            f"with an average consumption of {low['energy']:.2f} W."
        )
    @staticmethod
    def highest_consuming_house(houses_df):

        top = houses_df.iloc[0]

        return (
            f"{top['house_id']} is the highest energy consumer "
            f"with a total usage of {top['total_energy']:.0f} units."
        )
        
    @staticmethod
    def weekend_summary(df):

      weekday = df[df["is_weekend"] == False]["avg_energy"].values[0]
      weekend = df[df["is_weekend"] == True]["avg_energy"].values[0]

      difference = ((weekend - weekday) / weekday) * 100

      if difference > 0:
        return (
            f"Weekend energy consumption is "
            f"{difference:.1f}% higher than weekdays."
        )
      else:
        return (
            f"Weekend energy consumption is "
            f"{abs(difference):.1f}% lower than weekdays."
        )
    @staticmethod
    def anomaly_summary(high_anomalies, low_anomalies):

        if high_anomalies.empty and low_anomalies.empty:
            return "✅ No significant energy anomalies detected."

        summary = []

        if not high_anomalies.empty:
            summary.append(
                f" {len(high_anomalies)} high-energy anomalies detected."
            )

        if not low_anomalies.empty:
            summary.append(
                f" {len(low_anomalies)} low-energy anomalies detected."
            )

        return "\n".join(summary)