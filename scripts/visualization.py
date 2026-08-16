"""
visualization.py

Part 3.3: Visualization

Purpose:
Load Monte Carlo simulation results and generate
visualizations of annual earthquake losses.

Outputs:
- Histogram
- Boxplot
- CDF
- Tail Risk Curve
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
# 3. CREATE VISUALIZATION FOLDER
# ============================================================

visualization_folder = project_root / "results" / "visualizations"

visualization_folder.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 4. HISTOGRAM
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    losses,
    bins=50
)

plt.xlabel("Total Annual Loss ($ billions)")
plt.ylabel("Number of Simulated Years")
plt.title("Distribution of Simulated Annual Earthquake Losses")

plt.tight_layout()

histogram_file = visualization_folder / "annual_loss_histogram.png"

plt.savefig(histogram_file, dpi=300)

plt.show()

plt.close()


# ============================================================
# 5. BOXPLOT
# ============================================================

plt.figure(figsize=(8, 6))

plt.boxplot(
    losses,
    orientation="vertical"
)

plt.ylabel("Total Annual Loss ($ billions)")
plt.title("Distribution of Simulated Annual Earthquake Losses")

plt.tight_layout()

boxplot_file = visualization_folder / "annual_loss_boxplot.png"

plt.savefig(boxplot_file, dpi=300)

plt.show()

plt.close()


# ============================================================
# 6. CUMULATIVE DISTRIBUTION FUNCTION (CDF)
# ============================================================

sorted_losses = np.sort(losses)

cumulative_probability = (
    np.arange(1, len(sorted_losses) + 1)
    / len(sorted_losses)
)

plt.figure(figsize=(10, 6))

plt.plot(
    sorted_losses,
    cumulative_probability
)

plt.xlabel("Total Annual Loss ($ billions)")
plt.ylabel("Probability of Loss Being Less Than or Equal To")
plt.title("Cumulative Distribution of Simulated Annual Losses")

plt.grid(True)

plt.tight_layout()

cdf_file = visualization_folder / "annual_loss_cdf.png"

plt.savefig(cdf_file, dpi=300)

plt.show()

plt.close()


# ============================================================
# 7. TAIL RISK CURVE
# ============================================================

loss_thresholds = np.linspace(
    losses.min(),
    losses.max(),
    200
)

exceedance_probabilities = [
    (losses > threshold).mean()
    for threshold in loss_thresholds
]

plt.figure(figsize=(10, 6))

plt.plot(
    loss_thresholds,
    exceedance_probabilities
)

plt.xlabel("Annual Loss Threshold ($ billions)")
plt.ylabel("Probability of Exceeding Threshold")
plt.title("Earthquake Annual Loss Tail Risk Curve")

plt.grid(True)

plt.tight_layout()

tail_risk_file = visualization_folder / "tail_risk_curve.png"

plt.savefig(tail_risk_file, dpi=300)

plt.show()

plt.close()


# ============================================================
# 8. OUTPUT SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("VISUALIZATIONS CREATED")
print("=" * 60)

print(f"Histogram:       {histogram_file}")
print(f"Boxplot:         {boxplot_file}")
print(f"CDF:             {cdf_file}")
print(f"Tail Risk Curve: {tail_risk_file}")