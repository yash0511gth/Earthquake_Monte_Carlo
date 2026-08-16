"""
monte_carlo.py

Part 3.1: Monte Carlo Simulation Engine

Purpose:
Combine the frequency and severity models to simulate
10,000 possible earthquake years and calculate total
annual financial loss for each year.
"""

from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# 1. PROJECT PATH
# ============================================================

# Get the project root folder
project_root = Path(__file__).resolve().parent.parent

# Build the path to the Excel input file
excel_file = project_root / "data" / "Data_Earthquake Monte Carlo.xlsx"

print("Reading file from:")
print(excel_file)


# ============================================================
# 2. LOAD MODEL PARAMETERS
# ============================================================

model_parameters = pd.read_excel(
    excel_file,
    sheet_name="model_parameters"
)

print("\n" + "=" * 60)
print("MODEL PARAMETERS")
print("=" * 60)
print(model_parameters)


# ============================================================
# 3. MONTE CARLO SETTINGS
# ============================================================

number_of_simulations = 10_000

print("\n" + "=" * 60)
print("MONTE CARLO SIMULATION")
print("=" * 60)
print(f"Number of simulated years: {number_of_simulations}")


# ============================================================
# 4. SIMULATE ANNUAL EARTHQUAKE LOSSES
# ============================================================

annual_losses = []

for simulation in range(1, number_of_simulations + 1):

    total_annual_loss = 0.0

    # Process each earthquake magnitude group
    for _, row in model_parameters.iterrows():

        magnitude = row["Magnitude Group"]
        lam = row["Average Annual Frequency (λ)"]

        loss_min = row["Loss Min ($ in billions)"]
        loss_max = row["Loss Max ($ in billions)"]

        # Generate number of earthquakes for this magnitude group
        earthquake_count = np.random.poisson(lam)

        # Skip groups without loss assumptions
        if loss_min == "-" or loss_max == "-":
            continue

        # Convert Excel values to numbers
        loss_min = float(loss_min)
        loss_max = float(loss_max)

        # Generate one loss for every earthquake
        if earthquake_count > 0:

            simulated_losses = np.random.uniform(
                loss_min,
                loss_max,
                earthquake_count
            )

            # Add all losses for this magnitude group
            total_annual_loss += simulated_losses.sum()

    # Store total loss for this simulated year
    annual_losses.append(total_annual_loss)


# ============================================================
# 5. CREATE RESULTS DATAFRAME
# ============================================================

simulation_results = pd.DataFrame({
    "Simulation Year": range(1, number_of_simulations + 1),
    "Total Annual Loss ($ billions)": annual_losses
})


# ============================================================
# 6. DISPLAY SAMPLE RESULTS
# ============================================================

print("\n" + "=" * 60)
print("SIMULATION RESULTS — FIRST 10 YEARS")
print("=" * 60)

print(simulation_results.head(10))


print("\n" + "=" * 60)
print("SIMULATION SUMMARY")
print("=" * 60)

print(
    f"Number of simulated years: "
    f"{len(simulation_results):,}"
)

print(
    f"Average annual loss: "
    f"${simulation_results['Total Annual Loss ($ billions)'].mean():.2f}B"
)

print(
    f"Maximum annual loss: "
    f"${simulation_results['Total Annual Loss ($ billions)'].max():.2f}B"
)


# ============================================================
# 7. SAVE RESULTS TO CSV
# ============================================================

results_folder = project_root / "results"

# Create results folder if it does not already exist
results_folder.mkdir(exist_ok=True)

csv_file = results_folder / "simulated_annual_losses.csv"

simulation_results.to_csv(
    csv_file,
    index=False
)

print("\n" + "=" * 60)
print("RESULTS SAVED")
print("=" * 60)
print(csv_file)