from abc import ABC
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
)

import pandas as pd


class BasePipeline(ABC):
    """This is the base pipeline object from which all pipelines derive.

    Each individual step of the pipeline is represented by a **method**.
    These **method**'s are intended to represent small pieces of
    business logic that are testable and as reusable as possible.

    Args:
        steps (Optional[List[str]]): The list of steps to be executed
            during the pipeline.
        options: Variables required by individual pipeline methods.
    """

    def __init__(self, steps: Optional[List[str]] = None, options=None) -> None:
        self.steps: List[str] = steps or []
        self.options: Dict[str, Any] = options or {}

        if not steps:
            raise ValueError("At least one step must be provided.")

    @property
    def pipeline_steps(self) -> List[Callable]:
        """Ordered list of transformations defining the pipeline.

        Returns:
            List[Callable]: Transformation functions to apply to the
                input data.
        """
        return [getattr(self, step) for step in self.steps]

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the transformations to the input data sequentially.

        This method applies the transformation functions defined in the
        `self.pipeline_steps` property to the input data, `df`, in order
        to transform the data.

        Args:
            df (pd.DataFrame): Input data to apply the pipeline to.

        Returns:
            pd.DataFrame: Output data, transformed by the pipeline.
        """
        # apply each step of the pipeline to the input data
        for step in self.pipeline_steps:
            df = step(df=df)

        return df
