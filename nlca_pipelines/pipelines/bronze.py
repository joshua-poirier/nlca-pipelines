# pylint: disable=bad-staticmethod-argument
# ^^^ Due to known pylint issue: https://github.com/pylint-dev/pylint/issues/5441

import json
import uuid
from typing import List, Optional

import pandas as pd

from ..validation import validate
from ._base import BasePipeline
from .options import BronzePipelineOptionsDict


class BronzePipeline(BasePipeline):
    """A pipeline to ingest data to the bronze tier.

    Bronze-tiered data is a raw representation decorated with some
    metadata. It is intended to represent the raw data (which is not
    ready for processing), but be ready for processing.

    This class provides methods to transform the raw data into a
    structured format for further processing. It includes steps such as
    serializing rows, adding metadata columns, and generating unique
    identifiers.

    Args:
        steps (Optional[List[str]]): The list of steps to be executed
            during the pipeline.
        options (Optional[BronzePipelineOptionsDict]): Variables used by
            steps in the pipeline.
    """

    def __init__(
        self,
        steps: Optional[List[str]] = None,
        options: Optional[BronzePipelineOptionsDict] = None,
    ) -> None:
        super().__init__(steps=steps, options=options)

    @staticmethod
    def add_id(df: pd.DataFrame) -> pd.DataFrame:
        """Add Id column.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Data with a new `id` column.
        """
        df["id"] = df.apply(lambda _: uuid.uuid4(), axis=1)

        return df

    @validate(required_opts=["skiprows"])
    def add_row_number(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add the `source_row_number` column.

        We add the `skiprows` attribute to the row number, so that the
        value corresponds to the row number in the original source file
        (some files often have multiple header rows).

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Data with a new `source_row_number` column.
        """
        df["source_row_number"] = range(len(df))
        df["source_row_number"] = df["source_row_number"] + self.options["skiprows"]

        return df

    @validate(required_opts=["source_created_at"])
    def add_source_created_at(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add the `source_created_at` column.

        The `source_created_at` column is when the file was created at
        its source.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Data with a new `source_created_at` column.
        """
        df["source_created_at"] = self.options["source_created_at"]

        return df

    @validate(required_opts=["source_name"])
    def add_source_name(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add the `source_name` column.

        The `source_name` is typically the filename of the source file.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Data with a new `source_name` column.
        """
        df["source_name"] = self.options["source_name"]

        return df

    @validate(required_opts=["source_updated_at"])
    def add_source_updated_at(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add the `source_updated_at` column.

        The `source_updated_at` is the timestamp of the source file.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Data with a new `source_updated_at` column.
        """
        df["source_updated_at"] = self.options["source_updated_at"]

        return df

    @validate(required_opts=["source_uri"])
    def add_source_uri(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add the `source_uri` column.

        The `source_uri` should be the web address, Google Drive link,
        or S3 archive path for the source file.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Data with a new `source_uri` column.
        """
        df["source_uri"] = self.options["source_uri"]

        return df

    @staticmethod
    def serialize_rows(df: pd.DataFrame) -> pd.DataFrame:
        """Serializes the input data into a JSON string.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Data with a new `source_row` column,
                containing the serialized JSON string representation of
                the input data.
        """
        # extract input columns (we want to drop these later)
        input_cols = df.columns.tolist()

        # serialize input data to json
        df["source_row"] = df.apply(lambda row: json.dumps(row.to_dict()), axis=1)

        # drop the original data rows
        df = df.drop(input_cols, axis=1)

        return df
