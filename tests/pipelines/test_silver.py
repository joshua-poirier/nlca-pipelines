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


@pytest.mark.parametrize(
    "col, value, expected",
    [
        pytest.param("direction", "Horizontal", "HORIZONTAL"),
        pytest.param("direction", "horizontal", "HORIZONTAL"),
        pytest.param("direction", "VERTICAL", "VERTICAL"),
        pytest.param("direction", "invalid", None),
        pytest.param("direction", "", None),
        pytest.param("welltype", "oil", "OIL"),
        pytest.param("welltype", "Gas ", "GAS"),
        pytest.param("welltype", "invalid", None),
        pytest.param("basin", "Anadarko", "ANADARKO"),
        pytest.param("basin", "PERMIAN ", "PERMIAN"),
        pytest.param("basin", "invalid", None),
        pytest.param("subbasin", "Central Eagle Ford", "CENTRAL EAGLE FORD"),
        pytest.param("subbasin", "invalid", None),
        pytest.param("state", "Texas ", "TEXAS"),
        pytest.param("state", "oklahoma ", None),
        pytest.param("county", "pecos", "PECOS"),
        pytest.param("county", "invalid", None),
    ],
)
def test_eliminate_invalid_values(col: str, value: str, expected: str) -> None:
    """Testing the `eliminate_invalid_values` method."""
    df: pd.DataFrame = pd.DataFrame({col: [value]})
    pipeline = SilverPipeline(
        steps=["eliminate_invalid_values"],
        options={"cols_to_elim_invalid_values": [col]},
    )
    actual: pd.DataFrame = pipeline.run(df=df)

    assert actual[col].iloc[0] == expected
