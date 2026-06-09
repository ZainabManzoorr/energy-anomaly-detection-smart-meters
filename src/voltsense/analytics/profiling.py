import pandas as pd 

class DataProfiler:
#Generates automatic data quality and energy insights
    def __init__(self, df: pd.DataFrame):
      self.df = df
      
#Basic Data Health Check
    def missing_values(self):
        return self.df.isnull().sum().sort_values(ascending=False)
    def duplicates(self):
        return self.df.duplicated().sum() 
    def shape(self):
        return self.df.shape
    def column_types(self):
        return self.df.dtypes
      
#Energy Analytics
    def numeric_summary(self):
        return self.df.describe()
    def house_wise_summary(self):
        if "house_id" not in self.df.columns:
            return "house_id column not found"
        return self.df.groupby("house_id").size().sort_values(ascending=False)
    def energy_distribution(self,energy_col):
      if energy_col not in self.df.columns:
          return f"{energy_col} column not found"
      return self.df[energy_col].describe()

#Data Quality Report
    def generate_report(self):
        missing_ratio = self.df.isnull().sum() / (self.df.shape[0] * self.df.shape[1])
        duplicate_ratio = self.df.duplicated().sum() / self.df.shape[0]
        score = 100 * (1- (missing_ratio + duplicate_ratio))
        return round(score,2)