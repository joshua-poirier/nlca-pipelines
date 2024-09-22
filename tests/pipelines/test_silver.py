import pandas as pd
import pytest

from nlca_pipelines.pipelines import SilverPipeline


@pytest.mark.parametrize("expected_col", ["id", "name", "age"])
def test_parse_json(bronze_df: pd.DataFrame, expected_col: str) -> None:
    """Testing the `parse_json` method."""
    pipeline = SilverPipeline(steps=["parse_json"])
    actual: pd.DataFrame = pipeline.run(df=bronze_df)

    assert expected_col in actual.columns


def test_filter_missing(bronze_df: pd.DataFrame) -> None:
    """Testing the `filter_missing` method."""
    bronze_df["empty_col"] = ""

    pipeline = SilverPipeline(
        steps=["filter_missing"], options={"cols_to_filter_missing": ["empty_col"]}
    )
    actual: pd.DataFrame = pipeline.run(df=bronze_df)

    assert "empty_col" in actual.columns
    assert actual.shape[0] == 0
