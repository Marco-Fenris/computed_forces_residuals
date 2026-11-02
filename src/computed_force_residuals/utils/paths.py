from pathlib import Path


def get_project_root() -> Path:
    """
    Returns the root directory of the project.
    """
    return Path(__file__).parents[3].resolve()


PROJECT_ROOT = get_project_root()
DATA_DIR = PROJECT_ROOT / "data"
TRAINING_DATA_DIR = DATA_DIR / "featurized"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
METRICS_DIR = OUTPUTS_DIR / "metrics"
