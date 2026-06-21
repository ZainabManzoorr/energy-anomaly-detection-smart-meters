import pandas as pd

class ConsumptionPatterns:
  def weekday_weekend_usage(self,df):
    weekday = (
      df[df["is_weekend"] == 0]
      ["aggregate"]
      .mean()
    )
    weekend = (
      df[df["is_weekend"] == 1]
      ["aggregate"]
      .mean()
    )
    return{
      "weekday": weekday,
      "weekend": weekend
    }
  def peak_hours(self, df):

    hourly_usage = (
        df.groupby("hour")["aggregate"]
        .mean()
        .sort_values(ascending=False)
    )

    return hourly_usage