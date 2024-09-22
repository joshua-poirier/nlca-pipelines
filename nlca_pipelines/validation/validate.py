# type: ignore

import logging
from functools import wraps
from typing import (
    Any,
    Callable,
    List,
    Optional,
)

import pandas as pd

logger = logging.getLogger()


def validate(
    required_cols: Optional[List[str]] = None, required_opts: Optional[List[str]] = None
) -> Callable:
    """Decorator to validate required cols and opts for class instance.

    A method/function decorated with this decorator will validate that
    the input dataframe has all the required columns to execute
    successfully. It will also validate that the class instance has all
    the required options set to execute successfully.

    Args:
        required_cols (Optional[List[str]]): List of required columns.
        required_opts (Optional[List[str]]): List of required options.

    Returns:
        Callable: Decorator function.

    Examples:
        `validate` is a decorator that can be used to validate the input
        dataframe before executing the decorated function. The decorator
        can be used with or without required columns or options.
        >>> class MyClass:
        ...     @validate(required_cols=["age"])
        ...     def func(self, df: pd.DataFrame) -> pd.DataFrame:
        ...         df["age2"] = df["age"] + 2

        If we pass in a dataframe that is missing a required column,
        the function will raise a `ValueError`.
        >>> df = pd.DataFrame({"name": ["Alice", "Bob"]})
        >>> my_class = MyClass()
        >>> my_class.func(df)
        ValueError: Missing required columns: age

        If we passin a dataframe that has the required column, the
        function will execute successfully.
        >>> df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [5, 7]})
        >>> my_class.func(df)
            name    age     age2
        0  Alice      5        7
        1    Bob      7        9

        The decorator preserves the `required_cols` and `required_opts`
        arguments as attributes of the decorated function. This is
        useful for documentation.
        >>> getattr(my_class.func, "required_cols")
        ['age']

        Those attributes can also be accessed from the class, not just
        the instance.
        >>> getattr(MyClass.func, "required_cols")
        ['age']

    Notes:
        Static methods and instance methods are supported. Class methods
        are not supported at this time.
    """

    required_cols = required_cols or []
    required_opts = required_opts or []

    def inner(
        func: Callable[[Any, pd.DataFrame], pd.DataFrame]
    ) -> Callable[[Any, pd.DataFrame], pd.DataFrame]:
        """Validates the input before calling the decorated function.

        Args:
            func (Callable): The function to be decorated.

        Returns:
            Callable: The decorated function.

        Raises:
            ValueError: If the input dataframe is missing any of the
                required columns or options.
        """
        # expose the decorator args as attributes of the method
        setattr(func, "required_cols", required_cols)
        setattr(func, "required_opts", required_opts)

        # wrap static methods
        if isinstance(func, staticmethod):

            @staticmethod
            @wraps(func)
            def wrapper(df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
                """Validate the input and execute the wrapped method.

                Args:
                    df (pd.DataFrame): Input dataframe to be validated.

                Returns:
                    pd.DataFrame: Validated dataframe.
                """
                if not all(col in df.columns for col in required_cols):
                    missing: List[str] = list(set(required_cols) - set(df.columns))
                    raise ValueError(f"Missing required columns: {', '.join(missing)}")

                if required_opts:
                    raise ValueError("Static methods cannot have `required_opts`.")

                return func(df, *args, **kwargs)

        # wrap instance methods
        else:

            @wraps(func)
            def wrapper(self, df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
                """Validate the input and execute the wrapped method.

                Args:
                    self: The instance of the class.
                    df (pd.DataFrame): Input dataframe to be validated.

                Returns:
                    pd.DataFrame: Validated dataframe.
                """
                if not all(col in df.columns for col in required_cols):
                    missing: List[str] = list(set(required_cols) - set(df.columns))
                    raise ValueError(f"Missing required columns: {', '.join(missing)}")

                if not all(opt in self.options for opt in required_opts):
                    raise ValueError(
                        f"Missing required options: {', '.join(required_opts)}"
                    )

                return func(df, *args, **kwargs)

        return wrapper

    return inner
