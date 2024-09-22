from typing import Optional

import pytest

from nlca_pipelines.validation.values import Cum12moil


@pytest.mark.parametrize(
    "cum12moil, expected",
    [
        pytest.param("44697", 44697),
        pytest.param("-44697", None),
        pytest.param("seventeen", None),
        pytest.param("invalid", None),
        pytest.param("", None),
    ],
)
def test_cum12moil(cum12moil: str, expected: Optional[int]) -> None:
    """Test `Cum12moil` validator object."""
    assert Cum12moil(cum12moil=cum12moil).cum12moil == expected
