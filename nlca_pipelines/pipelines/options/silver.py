from typing import List

from typing_extensions import TypedDict


class SilverPipelineOptionsDict(TypedDict, total=False):
    """Enforces typing for the `options` used by the `SilverPipeline`.

    Attributes:
        cols_to_elim_invalid_values (List[str]): List of columns to
            eliminate invalid values for.
        cols_to_filter_missing (List[str]): List of columns to filter
            out all rows with missing values.
        cols_to_impute_with_mean (List[str]): List of columns to impute
            missing values with the mean.
        cols_to_impute_with_mode (List[str]): List of columns to impute
            missing values with the mode.
    """

    cols_to_elim_invalid_values: List[str]
    cols_to_filter_missing: List[str]
    cols_to_impute_with_mean: List[str]
    cols_to_impute_with_mode: List[str]
