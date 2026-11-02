from computed_force_residuals.constants import COMP_FORCE_COLS_MAP
import pandas as pd
from sklearn.metrics import r2_score
from scipy.stats import pearsonr


def compute_correlations(df):
    corr = {}
    for meas_col, comp_col in COMP_FORCE_COLS_MAP.items():
        corr[meas_col] = pearsonr(df[meas_col], df[comp_col])[0]

    print(f"Correlation: {corr}")
    return corr


def compute_r2_score(df):
    r2 = {}
    for meas_col, comp_col in COMP_FORCE_COLS_MAP.items():
        r2[meas_col] = r2_score(df[meas_col], df[comp_col])

    print(f"r2: {r2}")
    return r2


def create_metrics_df(df):
    corr = compute_correlations(df)
    r2 = compute_r2_score(df)

    metrics_df = pd.DataFrame({"correlation": corr, "r2": r2})
    return metrics_df
