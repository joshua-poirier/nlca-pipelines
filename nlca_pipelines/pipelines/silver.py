# pylint: disable=bad-staticmethod-argument
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
        # pylint: disable=cell-var-from-loop
        for col in self.options["cols_to_elim_invalid_values"]:
            # retrieve the validator object for the column
            validator: Callable = getattr(values, col.capitalize())
            if not validator:
                raise ValueError(f"No matching validator for '{col}'.")

            # apply the validator to all rows
            df[col] = df[col].apply(
                lambda x: getattr(validator(**{col.lower(): x}), col.lower()),
            )
        # pylint: enable=cell-var-from-loop

        return df
