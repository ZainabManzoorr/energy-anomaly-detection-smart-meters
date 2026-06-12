from voltsense.ingestion.multi_loader import MultiHouseDataLoader
from voltsense.analytics.profiling import DataProfiler

# Load data
loader = MultiHouseDataLoader("data/raw/refit_extracted")
df = loader.load_all()

# Profiling
profiler = DataProfiler(df)

print("SHAPE:", profiler.shape())
print("\nMISSING VALUES:\n", profiler.missing_values())
print("\nDUPLICATES:", profiler.duplicates())
print("\nHOUSE DISTRIBUTION:\n", profiler.house_wise_summary())
print("\nQUALITY SCORE:", profiler.generate_report())