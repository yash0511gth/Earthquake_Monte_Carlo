# Monte Carlo Simulation of United States Earthquake Risk (2000–2012)

## Problem Statement

How financially damaging could earthquakes be for a hypothetical insurer in the United States?

## Project Overview

This project develops a Monte Carlo simulation model to estimate potential annual earthquake losses using historical earthquake frequency data and financial loss assumptions.

The model uses:

- Poisson distribution for earthquake frequency modeling
- Uniform distribution for loss severity modeling
- Monte Carlo simulation to generate thousands of possible annual loss scenarios

## Data Sources

**Earthquake frequency and magnitude data:**  
U.S. Geological Survey (USGS), Earthquake Hazards Program — Lists, Maps, and Statistics

**Loss assumptions:**  
Federal Reserve Bank of Kansas City, *Economic Damage from Large Earthquakes*

Detailed sources, assumptions, and methodology are documented in `docs/MODEL_DEVELOPMENT.md`.

## Current Progress

### Completed

- Data preparation and model parameter setup
- Frequency modeling — `scripts/frequency_model.py`
- Severity modeling — `scripts/severity_model.py`
- Monte Carlo simulation engine — `scripts/monte_carlo.py`
- Risk metrics — `scripts/risk_metrics.py`
- Python visualizations — `scripts/visualization.py`
- Tableau presentation — `tableau/earthquake_risk_dashboard.twbx`

### Next

- Evaluation report
- Model interpretation and discussion
- Model limitations and assumptions
- Final conclusions and references