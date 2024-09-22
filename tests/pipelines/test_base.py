from typing import List

import pandas as pd
import pytest


def test_run(df: pd.DataFrame, sample_pipeline) -> None:
    """This tests the run method of the `BasePipeline`."""
    pipeline = sample_pipeline(
        steps=["step_one", "step_two", "step_three"],
        options={"force_upper": True},
    )

    actual = pipeline.run(df=df)

    assert actual.shape[0] == 2
    for col in ["name", "age", "first_name", "step_two", "step_three"]:
        assert col in actual.columns

    assert actual["name"].iloc[0] == "Alice Amore"
    assert actual["age"].iloc[0] == 5
    assert actual["first_name"].iloc[0] == "Alice"
    assert actual["step_two"].iloc[0] == "ALICE"
    assert actual["step_three"].iloc[0] == 3


@pytest.mark.parametrize(
    "steps",
    [
        pytest.param(["step_one", "step_two", "step_three"], id="3-sequentially"),
        pytest.param(["step_three", "step_two", "step_one"], id="3-reversed"),
        pytest.param(["step_one", "step_one"], id="first-repeated-twice"),
        pytest.param(["step_one"], id="first-only"),
    ],
)
def test_pipeline_steps(sample_pipeline, steps: List[str]) -> None:
    """Test the `pipeline_steps` property."""
    pipeline = sample_pipeline(steps=steps)

    assert len(pipeline.pipeline_steps) == len(steps)
    for i, step in enumerate(steps):
        assert pipeline.pipeline_steps[i].__name__ == step


@pytest.mark.parametrize(
    "method, required_cols",
    [
        pytest.param("step_one", ["name"], id="step_one"),
        pytest.param("step_two", ["first_name"], id="step_two"),
    ],
)
def test_required_cols(sample_pipeline, method: str, required_cols: List[str]) -> None:
    """Test that `required_cols` gets set as a method attribute."""
    pipeline = sample_pipeline(steps=[method])
    for col in required_cols:
        assert col in getattr(getattr(pipeline, method), "required_cols")


def test_required_opts(sample_pipeline) -> None:
    """Test that `required_opts` gets set as a method attribute."""
    pipeline = sample_pipeline(steps=["step_two"])
    assert "force_upper" in getattr(getattr(pipeline, "step_two"), "required_opts")
