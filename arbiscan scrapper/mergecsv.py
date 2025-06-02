import os
import pandas as pd

# Path to the folder containing all CSVs
RESULTS_DIR = "results"

# Gather all .csv filenames in RESULTS_DIR
csv_files = [
    os.path.join(RESULTS_DIR, fname)
    for fname in os.listdir(RESULTS_DIR)
    if fname.lower().endswith(".csv")
]

# Read each CSV into a DataFrame, then concatenate
dataframes = [pd.read_csv(path) for path in csv_files]
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a new CSV
combined_df.to_csv("combined_output.csv", index=False)

print(f"Combined {len(csv_files)} files into combined_output.csv")
