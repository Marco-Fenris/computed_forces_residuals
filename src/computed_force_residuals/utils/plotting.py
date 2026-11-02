import matplotlib.pyplot as plt
from computed_force_residuals.constants import FORCE_COLS,COMP_FORCE_COLS_MAP,AMTI_TO_FORCE_COLS_MAP

#Plots with DF
def plot_computed_measured_forces(df,swing_id=None):
    df_copy = df.copy()
    if swing_id:
        df_copy = df_copy.loc[df_copy.swing_id==swing_id]
    assert df_copy.swing_id.nunique() == 1, "df contains more than one swing id!"
    swing_id = df_copy.swing_id.unique()[0]
    fig, axes = plt.subplots(3,3, figsize=(16,16))
    axes = axes.flatten()
    i = 0
    for meas_col, comp_col in COMP_FORCE_COLS_MAP.items():
        axes[i].plot(df_copy[meas_col],label=meas_col)
        axes[i].plot(df_copy[comp_col],label=comp_col,linestyle="--")
        axes[i].set_title(meas_col)
        fig.suptitle(swing_id)