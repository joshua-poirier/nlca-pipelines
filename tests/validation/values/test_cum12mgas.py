from typing import Optional

import pytest

from nlca_pipelines.validation.values import Cum12mgas


@pytest.mark.parametrize(
    "cum12mgas, expected",
    [
        pytest.param("44697", 44697),
        pytest.param("-44697", None),
        pytest.param("seventeen", None),
        pytest.param("invalid", None),
        pytest.param("", None),
    ],
)
def test_cum12mgas(cum12mgas: str, expected: Optional[int]) -> None:
    """Test `Cum12mgas` validator object."""
    assert Cum12mgas(cum12mgas=cum12mgas).cum12mgas == expected
