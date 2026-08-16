"""
risk_metrics.py

Part 3.2: Risk Metrics

Purpose:
Load the Monte Carlo simulation results and calculate
summary statistics and tail-risk measures.
"""

from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# 1. PROJECT PATH
# ============================================================

project_root = Path(__file__).resolve().parent.parent

csv_file = project_root / "results" / "simulated_annual_losses.csv"

print("Reading simulation results from:")
print(csv_file)


# ============================================================
# 2. LOAD SIMULATION RESULTS
# ============================================================

simulation_results = pd.read_csv(csv_file)

losses = simulation_results["Total Annual Loss ($ billions)"]


# ============================================================
# 3. BASIC SUMMARY STATISTICS
# ============================================================

mean_loss = losses.mean()
median_loss = losses.median()
minimum_loss = losses.min()
maximum_loss = losses.max()

first_quartile = losses.quantile(0.25)
third_quartile = losses.quantile(0.75)


# ============================================================
# 4. PERCENTILE RISK
# ============================================================

percentile_95 = losses.quantile(0.95)
percentile_99 = losses.quantile(0.99)


# ============================================================
# 5. TAIL RISK
# ============================================================

# Define a loss threshold
threshold = 200.0

probability_exceeding_threshold = (
    (losses > threshold).mean()
)


# ============================================================
# 6. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("EARTHQUAKE LOSS RISK METRICS")
print("=" * 60)

print(f"Number of simulated years: {len(losses):,}")

print("\nSummary Statistics")
print("-" * 40)

print(f"Mean annual loss:       ${mean_loss:.2f}B")
print(f"Median annual loss:     ${median_loss:.2f}B")
print(f"Minimum annual loss:    ${minimum_loss:.2f}B")
print(f"Maximum annual loss:    ${maximum_loss:.2f}B")

print("\nQuartiles")
print("-" * 40)

print(f"25th percentile:         ${first_quartile:.2f}B")
print(f"75th percentile:         ${third_quartile:.2f}B")

print("\nPercentile Risk")
print("-" * 40)

print(f"95th percentile:         ${percentile_95:.2f}B")
print(f"99th percentile:         ${percentile_99:.2f}B")

print("\nTail Risk")
print("-" * 40)

print(f"Loss threshold:          ${threshold:.2f}B")
print(
    f"Probability of exceeding threshold: "
    f"{probability_exceeding_threshold:.2%}"
)


# ============================================================
# 7. SAVE RISK METRICS
# ============================================================

metrics = pd.DataFrame({
    "Metric": [
        "Mean",
        "Median",
        "Minimum",
        "25th Percentile",
        "75th Percentile",
        "Maximum",
        "95th Percentile",
        "99th Percentile",
        "Threshold",
        "Probability Exceeding Threshold"
    ],
    "Value": [
        mean_loss,
        median_loss,
        minimum_loss,
        first_quartile,
        third_quartile,
        maximum_loss,
        percentile_95,
        percentile_99,
        threshold,
        probability_exceeding_threshold
    ]
})


results_folder = project_root / "results"

metrics_file = results_folder / "risk_metrics.csv"

metrics.to_csv(
    metrics_file,
    index=False
)


print("\n" + "=" * 60)
print("RISK METRICS SAVED")
print("=" * 60)

print(metrics_file)


# ============================================================
# 8. GENERATE TAIL RISK CURVE DATA
# ============================================================

print("\n" + "=" * 60)
print("TAIL RISK CURVE DATA")
print("=" * 60)

# Create 100 loss thresholds across the simulated loss range
thresholds = np.linspace(
    minimum_loss,
    maximum_loss,
    100
)

# Calculate probability of exceeding each threshold
tail_risk_probabilities = []

for loss_threshold in thresholds:

    probability = (
        (losses > loss_threshold).mean()
    )

    tail_risk_probabilities.append(probability)


# Create DataFrame for Tableau
tail_risk = pd.DataFrame({
    "Loss Threshold ($ billions)": thresholds,
    "Probability of Exceeding": tail_risk_probabilities
})


# Save tail-risk data
tail_risk_file = results_folder / "tail_risk.csv"

tail_risk.to_csv(
    tail_risk_file,
    index=False
)


print("Tail risk data saved to:")
print(tail_risk_file)