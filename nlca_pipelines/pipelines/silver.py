# pylint: disable=bad-staticmethod-argument,cell-var-from-loop
# ^^^ Due to known pylint issue: https://github.com/pylint-dev/pylint/issues/5441

from typing import (
    Callable,
    List,
    Optional,
)

import pandas as pd

from ..validation import validate, values
from ._base import BasePipeline
from .options import SilverPipelineOptionsDict


class SilverPipeline(BasePipeline):
    """A pipeline to process data to the silver tier.

    The silver-tier represents filtered, cleaned, and augmented data. It
    has a defined structure with enforced schema (evolving as needed).

    This class provides methods to transform the bronze-tier into
    a structured format. It includes steps to parse JSON serialized
    data, filter invalid rows, impute missing values, and sort.

    Args:
        steps (Optional[List[str]]): The list of steps to be executed
            during the pipeline.
        options (Optional[SilverPipelineOptionsDict]): Variables used by
            steps in the pipeline.
    """

    def __init__(
        self,
        steps: Optional[List[str]] = None,
        options: Optional[SilverPipelineOptionsDict] = None,
    ) -> None:
        super().__init__(steps=steps, options=options)

    def parse_json(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse source data from the bronze-tier.

        Bronze-tier data typically stores the raw data as a JSON string.
        Here, we parse the serialized data into columns. Generally, this
        should be the first step in a silver pipeline.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Output data, with source data parsed into
                columns.
        """
        # extract the input columns (to be dropped later)
        input_cols: List[str] = [col for col in df.columns.tolist() if col != "id"]

        # parse the serialized JSON data
        df = df.join(pd.json_normalize(df["source_row"].apply(eval)))

        # drop the original input columns
        df = df.drop(input_cols, axis=1)

        return df

    @validate(required_opts=["cols_to_filter_missing"])
    def filter_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter invalid rows.

        Some rows **must** have values in order to be valid. Here, we
        filter rows with missing/empty values.

        Args:
            df (pd.DataFrame): Inpput data.

        Returns:
            pd.DataFrame: Output data, having invalid rows filtered out.
        """
        # filter out nulls
        df = df.dropna(subset=self.options["cols_to_filter_missing"])

        # filter out empty strings
        for col in self.options["cols_to_filter_missing"]:
            df = df[df[col] != ""]

        return df

    @validate(required_opts=["cols_to_elim_invalid_values"])
    def eliminate_invalid_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Eliminate invalid values.

        If a value is not the correct type, replace it with a null
        value.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Output data, with the relevant columns having
                invalid values replaced with nulls.
        """
        for col in self.options["cols_to_elim_invalid_values"]:
            # retrieve the validator object for the column
            validator: Optional[Callable] = getattr(values, col.capitalize())
            if validator is None:
                raise ValueError(f"No matching validator for '{col}'.")

            # apply the validator to all rows
            df[col] = df[col].apply(
                lambda x: getattr(validator(**{col.lower(): x}), col.lower()),
            )

        return df

    def impute_with_mean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Impute missing values with the mean value.

        Replace missing values in each column with the mean value of
        that column.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Output data, with missing values imputed with
                the mean for the relevant columns.
        """
        for col in self.options["cols_to_impute_with_mean"]:
            df[col] = df[col].fillna(df[col].mean())

        return df

    def impute_with_mode(self, df: pd.DataFrame) -> pd.DataFrame:
        """Impute missing values with the mode value.

        Replace missing values in each column with the mode value of
        that column (the most common value).

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Output data, with missing values imputed with
                the mode for the relevant columns.
        """
        for col in self.options["cols_to_impute_with_mode"]:
            df[col] = df[col].fillna(df[col].mode()[0])

        return df

    def sort(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sort by the values.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Output data, sorted in ascending order by the
                given columns.
        """
        return df.sort_values(by=self.options["cols_to_sort_by"])
