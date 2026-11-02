from computed_force_residuals.utils.paths import PROJECT_ROOT


def test_project_root():
    assert (
        PROJECT_ROOT / "pyproject.toml"
    ).exists(), "Project Root does not contain pyproject.toml. Is {PROJECT_ROOT} the project root?"
