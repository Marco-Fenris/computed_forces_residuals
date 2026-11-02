from pathlib import Path


def required_dir(path: str | Path):
    """Check if the directory exists. If not, raise an error."""
    path = Path(path)
    if not path.is_dir():
        raise ValueError(f"Directory does not exist: {path}")
    return path
