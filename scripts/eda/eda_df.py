import pandas as pd
from pathlib import Path
from computed_force_residuals.eval.metrics import create_metrics_df
from computed_force_residuals.utils.provanence import file_sha256
from computed_force_residuals.utils.fileio import required_dir
from computed_force_residuals.utils.paths import METRICS_DIR


def generate_metric_csv(dataset_p: str | Path, output_dir):
    dataset_p = Path(dataset_p)
    df = pd.read_parquet(dataset_p)

    metrics_df = create_metrics_df(df)

    sha256_hash = file_sha256(dataset)
    metrics_df = metrics_df.assign(sha256=sha256_hash, dataset=dataset_p.name)

    output_path = output_dir / f"{dataset_p.stem}.csv"

    required_dir(output_path.parent)  # check parent folder exists

    if output_path.exists():
        raise ValueError(f"CSV already exists at {output_path}")

    metrics_df.to_csv(output_path, index=False)
    print(f"Metric csv saved to {output_path}")


if __name__ == "__main__":
    dataset = r"C:\Users\Marco Chow\Desktop\Projects\Force_predictions\computed_force_residuals\data\featurized\u2_011026_240fps_combinedModel.parquet"
    output_path = METRICS_DIR / "datasets" / "featurized"

    generate_metric_csv(dataset, output_path)
