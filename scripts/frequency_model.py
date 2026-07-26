"""
frequency_model.py

Part 2: Frequency Modeling

Purpose:
Read the earthquake model parameters from Excel.
"""

from pathlib import Path
import pandas as pd
import numpy as np

# Get the project root folder
project_root = Path(__file__).resolve().parent.parent

# Build the full path to the Excel file
excel_file = project_root / "data" / "Data_Earthquake Monte Carlo.xlsx"

print("Reading file from:")
print(excel_file)

# Read the model_parameters worksheet
model_parameters = pd.read_excel(
    excel_file,
    sheet_name="model_parameters"
)

print("=" * 60)
print("EARTHQUAKE MODEL PARAMETERS")
print("=" * 60)
print(model_parameters)

print("\n" + "=" * 60)
print("DATA SUMMARY")
print("=" * 60)
model_parameters.info()

print("\n" + "=" * 60)
print("SIMULATED EARTHQUAKE YEAR")
print("=" * 60)

for _, row in model_parameters.iterrows():
    magnitude = row["Magnitude Group"]
    lam = row["Average Annual Frequency (λ)"]

    simulated_count = np.random.poisson(lam)

    print(f"{magnitude}: λ = {lam:.2f}, Simulated Count = {simulated_count}")
    
