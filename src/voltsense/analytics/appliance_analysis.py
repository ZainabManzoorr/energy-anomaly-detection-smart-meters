import pandas as pd


class ApplianceAnalyzer:
  
  APPLIANCE_COLS = [
        "appliance1",
        "appliance2",
        "appliance3",
        "appliance4",
        "appliance5",
        "appliance6",
        "appliance7",
        "appliance8",
        "appliance9",
  ]
  
  def total_consumption(self,df):
    totals = (
      df[self.APPLIANCE_COLS]
      .sum()
      .sort_values(ascending=False)
    )
    return totals
  
  def percentage_contribution(self,df):
    totals = self.total_consumption(df)
    
    percentages = (
      totals / totals.sum()
    ) * 100
    return percentages
    