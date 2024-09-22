from typing import List

from typing_extensions import TypedDict


class SilverPipelineOptionsDict(TypedDict, total=False):
    """Enforces typing for the `options` used by the `SilverPipeline`.

    Attributes:
        cols_to_elim_invalid_values (List[str]): List of columns to
            eliminate invalid values for.
        cols_to_filter_missing (List[str]): List of columns to filter
            out all rows with missing values.
    """

    cols_to_elim_invalid_values: List[str]
    cols_to_filter_missing: List[str]
