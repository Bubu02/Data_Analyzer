import pandas as pd
from ydata_profiling import ProfileReport
import json

# Load the file paths from the JSON file
with open("./paths/paths.json") as f:
    file_paths = json.load(f)

df = pd.read_excel(file_paths["DEMO_EXCEL"]) # Data set
print(df)

# Generate a report
profile = ProfileReport(df)
profile.to_file(output_file="./reports/Data.html") # HTML Name