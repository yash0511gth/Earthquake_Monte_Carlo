# Monte Carlo Simulation of United States Earthquake Risk 2000–2012

## Problem Statement

How financially damaging could earthquakes be for a hypothetical insurer in the United States?

This project uses historical U.S. earthquake frequency data from 2000–2012 and financial loss assumptions by earthquake magnitude to develop a Monte Carlo simulation of annual earthquake losses.

The objective is to estimate the range and probability of potential annual financial losses and use the simulated results to understand the potential tail risk faced by a hypothetical insurer.

## Part 1 — Data Set

### 1.1 Earthquake Frequency and Magnitude Data

Historical earthquake frequency data for the United States from 2000–2012 was collected from the U.S. Geological Survey (USGS).

The data records the number of earthquakes occurring in each year by magnitude category. The magnitude categories used in the dataset are:

- 5–5.9
- 6–6.9
- 7–7.9
- 8+

The historical frequency data was organized in Excel, with each row representing a magnitude group and each column representing a year from 2000 through 2012.

Source: U.S. Geological Survey (USGS), Earthquake Hazards Program — Lists, Maps, and Statistics.

https://www.usgs.gov/programs/earthquake-hazards/lists-maps-and-statistics

### 1.2 Earthquake Loss Assumptions

Financial loss assumptions were then added to the dataset to represent the potential economic damage associated with different earthquake magnitudes.

The loss ranges were based on information from the Federal Reserve Bank of Kansas City discussing the economic damage associated with large earthquakes.

The assumptions used in the model are:

| Magnitude Group | Minimum Loss ($ billions) | Maximum Loss ($ billions) |
|---|---:|---:|
| 5.5–6.5 | 0.1 | 2 |
| 6.5–7.5 | 1 | 15 |
| 7.5+ | 15 | 100 |

These ranges are modeling assumptions rather than exact historical losses for every earthquake in the dataset. They provide a severity range that can later be sampled during the simulation.

Source: Federal Reserve Bank of Kansas City, *Economic Damage from Large Earthquakes*.

https://www.kansascityfed.org/oklahomacity/oklahoma-economist/2016q1-economic-damage-large-earthquakes/

### 1.3 Excel Data Organization

The collected data was organized into a single Excel workbook with three worksheets:

1. **frequency_data** — historical earthquake counts by magnitude and year, including the calculated average annual frequency.
2. **loss_assumption** — minimum and maximum financial loss assumptions for each magnitude group.
3. **model_parameters** — the frequency and severity parameters brought together for use by the Python model.

The Excel workbook serves as the input dataset for the modeling scripts.

## Part 2 — Modeling

The modeling stage converts the historical data and loss assumptions prepared in Part 1 into parameters that can be used for stochastic simulation.

Two separate components were developed:

1. Frequency Modeling — models how many earthquakes may occur in a simulated year.
2. Severity Modeling — models the financial loss associated with an earthquake.

The two components will later be combined in the Monte Carlo simulation.

### 2.1 Frequency Modeling

#### Objective

The objective of frequency modeling is to estimate the number of earthquakes that could occur in a simulated year for each magnitude group.

The historical earthquake counts from 2000–2012 were used to calculate the average annual frequency, which serves as the Poisson parameter (λ).

The resulting parameters were:

| Magnitude Group | Average Annual Frequency (λ) |
|---|---:|
| 5–5.9 | 55.8462 |
| 6–6.9 | 5.6154 |
| 7–7.9 | 0.6154 |
| 8+ | 0.0000 |

#### Model: Poisson Distribution

A Poisson distribution was selected because the model is concerned with the number of earthquake events occurring within a fixed period of time (one year).

For each magnitude group, the average annual frequency is used as λ. A random earthquake count is then generated for a simulated year.

The Python implementation uses NumPy's `random.poisson()` function.

#### Python Implementation

The frequency model was built in several stages.

**1. Project path extraction**

`pathlib.Path` was used to identify the project root directory and construct the path to the Excel input file. This allows the script to locate the dataset without relying on a fixed computer-specific file path.

**2. Data loading**

`pandas.read_excel()` was used to read the `model_parameters` worksheet from the Excel workbook.

The worksheet provides the magnitude groups and their corresponding average annual frequencies.

**3. Parameter inspection**

The script prints the model parameters and uses `DataFrame.info()` to verify the structure and data types of the imported dataset.

**4. Frequency simulation**

The script loops through each magnitude group using `DataFrame.iterrows()`.

For each row:

- The magnitude group is identified.
- The average annual frequency (λ) is retrieved.
- NumPy's `np.random.poisson()` generates a simulated earthquake count.

The resulting output represents one possible earthquake year.

**Libraries used:**

- `pathlib` — project path and file-location management
- `pandas` — Excel data loading and DataFrame manipulation
- `numpy` — Poisson random sampling

The implementation is contained in:

`scripts/frequency_model.py`

---

### 2.2 Severity Modeling — Financial Loss

#### Objective

The objective of severity modeling is to estimate the potential financial loss associated with an earthquake within each magnitude group.

The loss assumptions prepared in Part 1 provide a minimum and maximum possible loss for each magnitude group.

The current model uses a Uniform Distribution to generate a financial loss within each specified range.

| Magnitude Group | Minimum Loss ($B) | Maximum Loss ($B) |
|---|---:|---:|
| 5.5–6.5 | 0.1 | 2 |
| 6.5–7.5 | 1 | 15 |
| 7.5+ | 15 | 100 |

#### Model: Uniform Distribution

A Uniform Distribution was selected for the initial severity model because it provides a straightforward way to generate a loss between the specified minimum and maximum assumptions.

Under this assumption, every value within the specified range has an equal probability of being selected.

This is an initial modeling assumption and will be discussed later when evaluating the realism of the model.

#### Python Implementation

The severity model was built in several stages.

**1. Project path extraction**

As with the frequency model, `pathlib.Path` was used to identify the project root and construct the path to the Excel workbook.

**2. Data loading**

`pandas.read_excel()` loads the `model_parameters` worksheet containing the magnitude groups and their loss ranges.

**3. Parameter inspection**

The script prints the imported model parameters and uses `DataFrame.info()` to inspect the structure and data types.

**4. Loss parameter extraction**

The script loops through each magnitude group using `DataFrame.iterrows()`.

For each row, the minimum and maximum loss assumptions are extracted.

**5. Missing loss assumptions**

The 8+ magnitude group currently has no corresponding loss assumptions because the historical dataset contains no 8+ earthquakes during the 2000–2012 period.

Rows containing `"-"` for the minimum or maximum loss are therefore skipped.

**6. Conversion to numeric values**

The loss values imported from Excel are converted to floating-point numbers using Python's `float()` function.

**7. Uniform loss simulation**

NumPy's `np.random.uniform()` function generates one random financial loss between the specified minimum and maximum values.

The simulated loss is reported in billions of dollars.

**Libraries used:**

- `pathlib` — project path and file-location management
- `pandas` — Excel data loading and DataFrame manipulation
- `numpy` — Uniform Distribution random sampling

The implementation is contained in:

`scripts/severity_model.py`

---

## Part 3 — Monte Carlo Simulation

The Monte Carlo stage combines the frequency and severity models developed in Part 2 to simulate possible annual earthquake losses.

The objective is to generate 10,000 possible earthquake years, calculate the total financial loss for each year, evaluate the resulting risk distribution, and visualize the results.

Part 3 consists of three components:

1. Monte Carlo Engine — combines Poisson frequency sampling and Uniform severity sampling.
2. Risk Metrics — calculates summary statistics, percentile risk, and tail risk.
3. Visualization — produces statistical plots in Python and presentation-ready visualizations in Tableau.

### 3.1 Monte Carlo Engine

#### Objective

The objective of the Monte Carlo engine is to simulate 10,000 possible earthquake years and calculate the total financial loss associated with each simulated year.

Each simulated year combines the two models developed in Part 2:

- Frequency model — determines how many earthquakes occur in each magnitude group using a Poisson distribution.
- Severity model — determines the financial loss associated with each earthquake using a Uniform Distribution.

The total annual loss is calculated by summing the simulated losses from all earthquake events occurring within each simulated year.

#### Python Implementation

The Monte Carlo script was built in several stages.

**1. Project path extraction**

`pathlib.Path` was used to identify the project root and construct the path to the Excel workbook containing the model parameters.

**2. Data loading**

`pandas.read_excel()` loads the `model_parameters` worksheet containing the average annual frequencies and financial loss ranges for each magnitude group.

**3. Simulation setup**

The simulation was configured to generate 10,000 independent simulated years.

**4. Frequency sampling**

For each simulated year and magnitude group, NumPy's `np.random.poisson()` function generates the number of earthquake events using the corresponding average annual frequency (λ).

**5. Severity sampling**

For each simulated earthquake event, NumPy's `np.random.uniform()` function generates a financial loss between the minimum and maximum loss assumptions for that magnitude group.

**6. Annual loss calculation**

The losses from all simulated earthquake events within a year are summed to produce the total annual financial loss.

**7. Results output**

The 10,000 simulated annual loss outcomes are stored in a CSV file for use in the risk metrics and visualization stages.

**Libraries used:**

- `pathlib` — project path and file-location management
- `pandas` — Excel data loading and DataFrame manipulation
- `numpy` — Poisson and Uniform random sampling

The implementation is contained in:

`scripts/monte_carlo.py`

Output:

`results/simulated_annual_losses.csv`

---

### 3.2 Risk Metrics

#### Objective

The objective of the risk metrics stage is to evaluate the distribution of simulated annual earthquake losses and quantify the potential financial exposure.

The analysis includes summary statistics, percentile risk measures, and tail-risk analysis.

#### Summary Statistics

The following statistics are calculated from the 10,000 simulated annual losses:

- Mean
- Median
- Minimum
- Maximum
- 25th percentile
- 75th percentile

The results from the current simulation are:

| Metric | Result |
|---|---:|
| Mean annual loss | $139.20B |
| Median annual loss | $125.67B |
| Minimum annual loss | $42.92B |
| Maximum annual loss | $498.37B |
| 25th percentile | $98.91B |
| 75th percentile | $169.60B |

#### Percentile Risk

Two high-loss percentiles were calculated:

| Risk Measure | Result |
|---|---:|
| 95th percentile | $244.54B |
| 99th percentile | $308.64B |

The 95th percentile represents a loss level exceeded by approximately 5% of simulated years.

The 99th percentile represents a loss level exceeded by approximately 1% of simulated years.

#### Tail Risk

A loss threshold of $200 billion was selected to evaluate exceedance risk.

The probability that simulated annual losses exceed this threshold is:

**13.62%**

This provides an initial measure of the probability of experiencing an annual loss above a defined financial threshold.

#### Python Implementation

`pandas` is used to load the Monte Carlo simulation results and calculate the statistical measures.

`numpy` is used for percentile calculations and numerical processing.

The script also generates a separate dataset containing exceedance probabilities across a range of loss thresholds. This dataset is used to construct the tail-risk curve in Tableau.

**Libraries used:**

- `pathlib` — project path and file-location management
- `pandas` — CSV loading, DataFrame creation, and statistical calculations
- `numpy` — numerical and percentile calculations

The implementation is contained in:

`scripts/risk_metrics.py`

Outputs:

- `results/risk_metrics.csv`
- `results/tail_risk.csv`

---

### 3.3 Visualization

The visualization stage presents the simulated annual loss distribution and the associated risk measures.

Two tools were used:

1. Python — generates the underlying statistical visualizations.
2. Tableau — presents the simulation results in an interactive, presentation-ready format.

#### Python Visualizations

The Python visualization script loads the simulated annual loss results from the Monte Carlo engine and produces four visualizations:

**1. Histogram**

Shows the distribution of the 10,000 simulated annual losses.

**2. Boxplot**

Shows the median, quartiles, overall spread, and potential high-loss outliers.

**3. Cumulative Distribution Function (CDF)**

Shows the cumulative probability of annual losses being less than or equal to a given loss level.

**4. Tail Risk Curve**

Shows the probability that annual loss exceeds a given loss threshold.

The implementation is contained in:

`scripts/visualization.py`

The visualizations are saved under:

`results/visualizations/`

#### Tableau Visualization

The Python-generated results were then loaded into Tableau to create presentation-ready versions of the same four visualizations:

- Annual Loss Distribution — Histogram
- Annual Loss Boxplot
- Annual Loss CDF
- Annual Earthquake Loss Tail Risk Curve

The Tableau workbook is stored in:

`tableau/earthquake_risk_dashboard.twbx`

The Tableau visualizations were validated against the Python risk calculations. In particular:

- $200B loss threshold → 13.62% exceedance probability
- 95th percentile → $244.54B
- 99th percentile → $308.64B

This ensures that the presentation layer is consistent with the underlying Python calculations.

---

## Part 4 — Risk Analysis

The evaluation stage uses the simulation results generated throughout Part 3 to develop a quantitative risk analysis of the modeled earthquake losses.

### 4.1 Simulation Results

This section presents and interprets the numerical results produced by the 10,000 simulated earthquake years, including:

- Overview
- Summary statistics
- Metric Interpretation
    -  Mean and median annual loss
    - Quartiles
    - 95th and 99th percentiles
    - Minimum and maximum simulated losses
    - Tail-risk measures
- Visualization of Simulation Results
    - Histogram
    - Boxplot
    - CDF
    - Tail-risk curve

### 4.2 Risk Interpretation


### 4.3 Risk Implications


The completed risk analysis will provide the transition from the technical simulation engine to the broader quantitative and practical interpretation of the model results.