from typing import Optional

import pytest

from nlca_pipelines.validation.values import Cum12mwater


@pytest.mark.parametrize(
    "cum12mwater, expected",
    [
        pytest.param("44697", 44697),
        pytest.param("-44697", None),
        pytest.param("seventeen", None),
        pytest.param("invalid", None),
        pytest.param("", None),
    ],
)
def test_cum12mwater(cum12mwater: str, expected: Optional[int]) -> None:
    """Test `Cum12mwater` validator object."""
    assert Cum12mwater(cum12mwater=cum12mwater).cum12mwater == expected
