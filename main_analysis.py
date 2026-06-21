from src.voltsense.ingestion.multi_loader import DataLoader
from src.voltsense.cleaning.clean import DataCleaner
from src.voltsense.features.feature import FeatureEngineer

from src.voltsense.analytics.appliance_analysis import ApplianceAnalyzer
from src.voltsense.analytics.consumption_patterns import ConsumptionPatterns
from src.voltsense.analytics.visualize import Visualizer


def run_analysis_pipeline():

    # --------------------
    # LOAD
    # --------------------
    loader = DataLoader()
    df = loader.load_data("data/raw/combined_refit.csv")

    print("Data loaded:", df.shape)

    # --------------------
    # CLEAN
    # --------------------
    cleaner = DataCleaner()
    df = cleaner.clean(df)

    print("Data cleaned:", df.shape)

    # --------------------
    # FEATURES
    # --------------------
    fe = FeatureEngineer()
    df = fe.transform(df)

    print("Features created:", df.shape)

    # --------------------
    # ANALYSIS LOGIC
    # --------------------
    analyzer = ApplianceAnalyzer()
    patterns = ConsumptionPatterns()
    viz = Visualizer()

    # Appliance contribution
    percentages = analyzer.percentage_contribution(df)

    # Hourly usage
    hourly_usage = patterns.peak_hours(df)

    # Weekday vs weekend
    usage = patterns.weekday_weekend_usage(df)
    weekday = usage["weekday"]
    weekend = usage["weekend"]

    # --------------------
    # VISUALIZATION
    # --------------------
    viz.plot_appliance_contribution(percentages)

    viz.plot_hourly_usage(hourly_usage)

    viz.plot_weekday_weekend(weekday, weekend)


if __name__ == "__main__":
    run_analysis_pipeline()