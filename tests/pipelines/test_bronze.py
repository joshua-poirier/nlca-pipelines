from datetime import datetime
from typing import List

import pandas as pd
import pytest

from nlca_pipelines.pipelines import BronzePipeline, BronzePipelineOptionsDict

NOW: datetime = datetime.now()


@pytest.mark.parametrize(
    "steps, options",
    [
        pytest.param(["serialize_rows"], {}, id="one-step-no-opts"),
        pytest.param(
            ["serialize_rows", "add_source_name"],
            {"source_name": "test"},
            id="multi-steps-with-opts",
        ),
    ],
)
def test_init(steps: List[str], options: BronzePipelineOptionsDict) -> None:
    """Test that the pipeline initializes correctly."""
    pipeline = BronzePipeline(steps=steps, options=options)

    # test steps are initialized correctly
    for step in steps:
        assert step in pipeline.steps

    # test options are initialized correctly
    for key, value in options.items():
        assert pipeline.options[key] == value


def test_add_id(df: pd.DataFrame) -> None:
    """Test that the `add_id` method adds an `id` column."""
    actual: pd.DataFrame = BronzePipeline.add_id(df=df)

    assert "id" in actual.columns


def test_add_row_number(df: pd.DataFrame) -> None:
    """Test the `add_row_number method`."""
    actual: pd.DataFrame = BronzePipeline(
        steps=["add_row_number"], options={"skiprows": 1}
    ).run(df=df)

    assert "source_row_number" in actual.columns
    assert actual["source_row_number"].iloc[0] == 1


def test_add_source_created_at(df: pd.DataFrame) -> None:
    """Test the `add_source_created_at` method."""
    actual: pd.DataFrame = BronzePipeline(
        steps=["add_source_created_at"],
        options={"source_created_at": NOW.strftime("%Y-%m-%d")},
    ).run(df=df)

    assert "source_created_at" in actual.columns
    assert actual["source_created_at"].iloc[0] == NOW.strftime("%Y-%m-%d")


def test_add_source_name(df: pd.DataFrame) -> None:
    """Test the `add_source_name` method."""
    actual: pd.DataFrame = BronzePipeline(
        steps=["add_source_name"], options={"source_name": "test"}
    ).run(df=df)

    assert "source_name" in actual.columns
    assert actual["source_name"].iloc[0] == "test"


def test_add_source_updated_at(df: pd.DataFrame) -> None:
    """Test the `add_source_updated_at` method."""
    actual: pd.DataFrame = BronzePipeline(
        steps=["add_source_updated_at"],
        options={"source_updated_at": NOW.strftime("%Y-%m-%d")},
    ).run(df=df)

    assert "source_updated_at" in actual.columns
    assert actual["source_updated_at"].iloc[0] == NOW.strftime("%Y-%m-%d")


def test_add_source_uri(df: pd.DataFrame) -> None:
    """Test the `add_source_uri` method."""
    actual: pd.DataFrame = BronzePipeline(
        steps=["add_source_uri"],
        options={"source_uri": "https://google.com/somefile.zip"},
    ).run(df=df)

    assert "source_uri" in actual.columns
    assert actual["source_uri"].iloc[0] == "https://google.com/somefile.zip"


def test_serialize_rows(df: pd.DataFrame) -> None:
    """Test that the `serialize_rows` method serializes data to json."""
    actual: pd.DataFrame = BronzePipeline.serialize_rows(df=df)

    assert "source_row" in actual.columns
    assert actual["source_row"].iloc[0] == '{"name": "Alice Amore", "age": 5}'
