import pandas as pd
import argparse
import yaml
from computed_force_residuals.utils.paths import TRAINING_DATA_DIR
from computed_force_residuals.utils.fileio import required_dir
from computed_force_residuals.constants import (
    COMP_FORCE_COLS_MAP,
    AMTI_TO_FORCE_COLS_MAP,
)
from computed_force_residuals.utils.plotting import plot_computed_measured_forces
from computed_force_residuals.eval.metrics import create_metrics_df
from pathlib import Path


def _invert_fp_channels(df):
    """Invert Fx and Fy of raw force plate readings to match force screen outputs"""
    assert all(
        flip_col in df.columns for flip_col in ["Fx_l", "Fy_l", "Fx_r", "Fy_r"]
    ), "One or more Force Columns missing from df"
    df["Fx_l"] = -df["Fx_l"]
    df["Fy_l"] = -df["Fy_l"]
    df["Fx_r"] = -df["Fx_r"]
    df["Fy_r"] = -df["Fy_r"]
    return df


def create_dataset(
    computed_force_pq: str | Path,
    unfeaturized_pose_force_pq: str | Path,
    featurized_pose_force_pq: str | Path,
    output_name: str,
) -> pd.DataFrame:
    """
    Create a dataset by merging computed forces with featurized pose forces. Add total measured force columns.
    Args:
        computed_force_pq: path to computed force parquet
        unfeaturized_pose_force_pq: path to unfeaturized pose force parquet
        featurized_pose_force_pq: path to featurized pose force parquet
        output_name: name of the output parquet
    Returns:
        pd.DataFrame with computed and measured forces along with features from featurized_pose_force_pq
    """
    computed_force_pq = Path(computed_force_pq)
    unfeaturized_pose_force_pq = Path(unfeaturized_pose_force_pq)
    featurized_pose_force_pq = Path(featurized_pose_force_pq)

    output_pq = required_dir(TRAINING_DATA_DIR)  # Check if folder exists
    output_pq = TRAINING_DATA_DIR / output_name

    if output_pq.exists():
        raise ValueError("Output parquet already exists!")

    computed_force_df = pd.read_parquet(computed_force_pq)
    computed_force_ids = computed_force_df.swing_id.unique().tolist()

    unfeaturized_pose_force_df = pd.read_parquet(unfeaturized_pose_force_pq)
    unfeaturized_pose_force_ids = unfeaturized_pose_force_df.swing_id.unique().tolist()

    # find mutual swing_ids
    mutual_swing_ids = list(
        set(computed_force_ids).intersection(set(unfeaturized_pose_force_ids))
    )

    # Only keep swings in Computed Forces DF that also exists in the Pose Force DF
    computed_force_df = computed_force_df[
        computed_force_df.swing_id.isin(mutual_swing_ids)
    ].reset_index(drop=True)

    # add frame column
    computed_force_df = computed_force_df.merge(
        unfeaturized_pose_force_df[["swing_id", "frame", "p_pos"]],
        on=["swing_id", "frame"],
        how="inner",
    )

    # Now read the featurized parquet()

    featurized_pose_force_df = pd.read_parquet(featurized_pose_force_pq)

    computed_force_ids = computed_force_df.swing_id.unique().tolist()

    computed_force_featurized_df = computed_force_df.merge(
        featurized_pose_force_df, on=["swing_id", "frame"], how="inner"
    )

    computed_force_featurized_df = computed_force_featurized_df.rename(
        columns=COMP_FORCE_COLS_MAP
    )
    computed_force_featurized_df = computed_force_featurized_df.rename(
        columns=AMTI_TO_FORCE_COLS_MAP
    )

    # Flip Fx and Fy channels from force plate readings to match that of Force Screen
    computed_force_featurized_df = _invert_fp_channels(computed_force_featurized_df)

    # Add measured force total
    computed_force_featurized_df["Fx_t"] = (
        computed_force_featurized_df["Fx_l"] + computed_force_featurized_df["Fx_r"]
    )
    computed_force_featurized_df["Fy_t"] = (
        computed_force_featurized_df["Fy_l"] + computed_force_featurized_df["Fy_r"]
    )
    computed_force_featurized_df["Fz_t"] = (
        computed_force_featurized_df["Fz_l"] + computed_force_featurized_df["Fz_r"]
    )

    # save df
    computed_force_featurized_df.to_parquet(output_pq)
    return computed_force_featurized_df


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config", type=Path, required=True, help="Path to config file"
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = arg_parser()

    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    create_dataset(
        computed_force_pq=cfg["computed_force_pq"],
        unfeaturized_pose_force_pq=cfg["unfeaturized_pose_force_pq"],
        featurized_pose_force_pq=cfg["featurized_pose_force_pq"],
        output_name=cfg["output_dataset_name"],
    )

    # plt_count = 0
    # for id, swing_df in computed_force_featurized_df.groupby("swing_id"):
    #     plot_computed_measured_forces(swing_df)
    #     plt_count += 1
    #     if plt_count > 5:
    #         break

    # metrics_df = create_metrics_df(computed_force_featurized_df)

    # corr_per_swing = computed_force_featurized_df.groupby("swing_id").apply(
    #     lambda g: pearsonr(g["Fz_t"], g["comp_Fz_t"])[0]
    # )
    # print(
    #     f"Corr Mean:{corr_per_swing.mean()}\nCorr std:{corr_per_swing.std()}\nCorr Median:{corr_per_swing.median()}\n"
    # )
