from typing import Any, Dict, List, Optional

import pandas as pd
import pytest

from nlca_pipelines.validation import validate


@pytest.fixture
def df() -> pd.DataFrame:
    """Reusable dataframe as a fixture."""
    return pd.DataFrame({"name": ["Alice", "Bob"], "age": [5, 7]})


@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param({}, id="no_args"),
        pytest.param({"required_cols": ["a"]}, id="single-req-col"),
        pytest.param({"required_cols": ["a", "b"]}, id="multi-req-cols"),
        pytest.param({"required_opts": ["a"]}, id="single-req-opt"),
        pytest.param({"required_opts": ["a", "b"]}, id="multi-req-opts"),
        pytest.param({"required_cols": ["a"], "required_opts": ["b"]}, id="both"),
    ],
)
def test_validate_decorator_preserves_args(kwargs: Dict[str, Any]) -> None:
    """Variotions on valid kwargs passed to the validate decorator.

    Args:
        kwargs (Dict[str, Any]): Dictionary of keyword arguments to pass
            to the decorator.
    """

    @validate(**kwargs)
    def func(df: pd.DataFrame) -> pd.DataFrame:
        return df
    
    for key, value in kwargs.items():
        assert getattr(func, key) == value


@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param({"something_wrong": ["a"]}, id="single-wrong-kwarg"),
        pytest.param(
            {"required_cols": ["a"], "something_wrong": ["b"]},
            id="single-right-single-wrong-kwargs",
        ),
        pytest.param(
            {"something_wrong1": ["a"], "something_wrong2": ["b"]},
            id="multi-wrong-kwargs",
        ),
    ],
)
def test_validate_decorator_raises_for_unexpected_args(kwargs: Dict[str, Any]) -> None:
    """Variations on invalid kwargs passed to hte validate decorator.

    Args:
        kwargs (Dict[str, Any]): Dictionary of keyword arguments to pass
            to the decorator.
    """
    with pytest.raises(TypeError):

        @validate(**kwargs)
        def _(df: pd.DataFrame) -> pd.DataFrame:
            return df


def test_validate_decorator_raises_when_staticmethod_given_required_opts(
    df: pd.DataFrame
) -> None:
    """Test that the validate decorator raises when required_opts are
    given to a staticmethod.

    The validate decorator should raise a ValueError when required_opts
    are given to a staticmethod. This is because the options are stored
    as an attribute of the instance and not the class; thereby, making
    them unavailable to static methods.
    """
    class A:
        @validate(required_opts=["a"])
        @staticmethod
        def func(df: pd.DataFrame) -> pd.DataFrame:
            return df

    with pytest.raises(ValueError) as exc_info:
        A.func(df)

    assert str(exc_info.value) == "Static methods cannot have `required_opts`."


def test_validate_decorator_raises_when_instance_method_missing_required_cols(
    df: pd.DataFrame
) -> None:
    """Test that the decorator raises for missing required columns.

    Here, we test for instance methods. The decorator should raise a
    ValueError when required columns are missing from the input
    dataframe.
    """
    # pylint: disable=bad-staticmethod-argument,unused-argument
    class A:
        @validate(required_cols=["first_name"])
        def func(self, df: pd.DataFrame) -> pd.DataFrame:
            return df

    # pylint: enable=bad-staticmethod-argument,unused-argument

    with pytest.raises(ValueError) as exc_info:
        # pylint: disable-next=no-value-for-parameter
        A().func(df=df)

    assert str(exc_info.value) == "Missing required columns: first_name"


def test_validate_decorator_raises_when_static_method_missing_required_cols(
    df: pd.DataFrame
) -> None:
    """Test that the decorator raises for missing required columns.

    Here, we test for static methods. The decorator should raise a
    ValueError when required columns are missing from the input
    dataframe.
    """
    class A:
        @validate(required_cols=["first_name"])
        @staticmethod
        def func(self, df: pd.DataFrame) -> pd.DataFrame:
            return df

    with pytest.raises(ValueError) as exc_info:
        A().func(df=df)

    assert str(exc_info.value) == "Missing required columns: first_name"


def test_validate_decorator_raises_when_instance_method_missing_required_opts(
    df: pd.DataFrame
) -> None:
    """Test that the validate decorator raises when required options are
    missing.

    The validate decorator should raise a ValueError when required
    options are missing from the pipeline instance.
    """
    # pylint: disable=bad-staticmethod-argument,unused-argument
    class A:
        def __init__(
            self,
            steps: Optional[List[str]] = None,
            options: Optional[Dict[str, Any]] = None,
        ) -> None:
            self.steps = steps
            self.options = options

        @validate(required_opts=["force_upper"])
        def func(self, df: pd.DataFrame) -> pd.DataFrame:
            return df

    # pylint: enable=bad-staticmethod-argument,unused-argument

    with pytest.raises(ValueError) as exc_info:
        # pylint: disable-next=no-value-for-parameter
        A(options={"other_option": "something"}).func(df=df)

    assert str(exc_info.value) == "Missing required options: force_upper"
