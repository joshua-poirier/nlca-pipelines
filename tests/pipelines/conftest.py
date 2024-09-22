# pylint: disable=bad-staticmethod-argument
# ^^^ Due to known pylint issue: https://github.com/pylint-dev/pylint/issues/5441

from datetime import datetime
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

import pandas as pd
import pytest

from nlca_pipelines.pipelines import BronzePipeline
from nlca_pipelines.pipelines._base import BasePipeline
from nlca_pipelines.validation import validate


class SamplePipeline(BasePipeline):
    """This is a sample pipeline used for testing.

    It is derived from the `BasePipeline` and intended for use testing
    the `BasePipeline`'s features.
    """

    def __init__(
        self,
        steps: Optional[List[str]] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(steps, options)

    @validate(required_cols=["name"])
    @staticmethod
    def step_one(df: pd.DataFrame) -> pd.DataFrame:
        """Extracts the first name from the `name` column.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Data with the `first_name` column added.
        """
        df["first_name"] = df["name"].str.split().str[0]

        return df

    @validate(required_cols=["first_name"], required_opts=["force_upper"])
    def step_two(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optionally forces the `first_name` column to uppercase.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Data with a `step_two` column added,
                containing the `first_name` column in uppercase if
                `force_upper` is `True`. Otherwise, the `first_name`
                column is returned as-is.
        """
        df["step_two"] = (
            df["first_name"].str.upper()
            if self.options["force_upper"]
            else df["first_name"]
        )

        return df

    @staticmethod
    def step_three(df: pd.DataFrame) -> pd.DataFrame:
        """Adds a `step_three` column with the value `3`.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Data with a `step_three` column added.
        """
        df["step_three"] = 3

        return df


@pytest.fixture(name="sample_pipeline")
def fixture_sample_pipeline():
    """Sample pipeline class as a fixture."""
    return SamplePipeline


@pytest.fixture(name="df")
def fixture_df() -> pd.DataFrame:
    """Reusable dataframe as a fixture."""
    return pd.DataFrame({"name": ["Alice Amore", "Bob Bogart"], "age": [5, 7]})


@pytest.fixture(name="bronze_df")
def fixture_bronze_df(df: pd.DataFrame) -> pd.DataFrame:
    """Reusable bronze-tier dataframe as a fixture."""
    bronze_pipeline = BronzePipeline(
        steps=[
            "serialize_rows",
            "add_source_name",
            "add_source_uri",
            "add_row_number",
            "add_source_updated_at",
            "add_id",
        ],
        options={
            "skiprows": 1,
            "source_created_at": datetime.now().strftime("%Y-%m-%d"),
            "source_name": "somefile.zip",
            "source_uri": "https://google.com/somefile.zip",
            "source_updated_at": datetime.now().strftime("%Y-%m-%d"),
        },
    )

    return bronze_pipeline.run(df=df)
