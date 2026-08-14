"""
severity_model.py

Part 3: Severity Modeling

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
print("SIMULATED EARTHQUAKE LOSSES")
print("=" * 60)

for _, row in model_parameters.iterrows():

    magnitude = row["Magnitude Group"]

    loss_min = row["Loss Min ($ in billions)"]
    loss_max = row["Loss Max ($ in billions)"]

    # Skip rows with no loss assumptions
    if loss_min == "-" or loss_max == "-":
        print(f"{magnitude}: No loss assumptions available.")
        continue

    # Convert Excel values to numbers
    loss_min = float(loss_min)
    loss_max = float(loss_max)

    # Simulate one financial loss
    simulated_loss = np.random.uniform(loss_min, loss_max)

    print(
        f"{magnitude}: "
        f"Loss Range = ${loss_min:.1f}B - ${loss_max:.1f}B, "
        f"Simulated Loss = ${simulated_loss:.2f}B"
    )