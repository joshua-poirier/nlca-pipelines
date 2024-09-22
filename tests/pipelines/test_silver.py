from datetime import datetime

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
        pytest.param("spuddate", "2023-07-01", datetime(2023, 7, 1)),
        pytest.param("spuddate", "2033-07-01", None),
        pytest.param("spuddate", "invalid", None),
        pytest.param("cum12moil", "44697", 44697),
        pytest.param("cum12moil", "seventten", None),
        pytest.param("cum12moil", "", None),
        pytest.param("cum12mgas", "44697", 44697),
        pytest.param("cum12mgas", "seventten", None),
        pytest.param("cum12mgas", "", None),
        pytest.param("cum12mwater", "44697", 44697),
        pytest.param("cum12mwater", "seventten", None),
        pytest.param("cum12mwater", "", None),
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


@pytest.mark.parametrize("col, expected", [("A", 3), ("B", 7)])
def test_impute_with_mean(col: str, expected: int) -> None:
    """Testing the `impute_with_mean` method."""
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2, None, 6], "B": [5, 7, None, 9]})
    pipeline = SilverPipeline(
        steps=["impute_with_mean"],
        options={"cols_to_impute_with_mean": ["A", "B"]},
    )

    actual: pd.DataFrame = pipeline.run(df=df)

    assert actual[col].iloc[2] == expected


def test_impute_with_mode() -> None:
    """Testing the `impute_with_mode` method."""
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2, 1, 2, 1, 2, 3, None]})
    pipeline = SilverPipeline(
        steps=["impute_with_mode"],
        options={"cols_to_impute_with_mode": ["A"]},
    )

    actual: pd.DataFrame = pipeline.run(df=df)

    assert actual["A"].iloc[7] == 1


def test_sort() -> None:
    """Testing the `sort` method."""
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2, 1, 3]})
    pipeline = SilverPipeline(
        steps=["sort"],
        options={"cols_to_sort_by": ["A"]},
    )

    actual: pd.DataFrame = pipeline.run(df=df)

    assert actual["A"].iloc[0] == 1
    assert actual["A"].iloc[1] == 1
    assert actual["A"].iloc[2] == 2
    assert actual["A"].iloc[3] == 3
