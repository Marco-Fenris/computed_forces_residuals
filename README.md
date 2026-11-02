# Computed Force Residuals

Python tools for preparing computed ground-reaction-force data, combining it with pose and force-plate data, and evaluating force residuals.

## Setup

Requires Python 3.12 or later.

```bash
python -m pip install -e ".[dev]"
```

## Project layout

- `src/computed_force_residuals/` — package utilities, force-column definitions, and evaluation metrics.
- `scripts/dataset/` — scripts for ingesting computed-force JSON files and assembling datasets.
- `scripts/eda/` — exploratory analysis and metric-generation scripts.
- `configs/` — training-data configuration files.
- `data/` — input and generated datasets.
- `outputs/` — generated outputs, including metrics.
- `tests/` — project tests.

Dataset scripts expect the input files and paths required by their functions; see each script for its arguments and examples. Generated training datasets are stored under `data/featurized/`, and metrics under `outputs/metrics/`.

Run the test suite with:

```bash
python -m pytest
```
