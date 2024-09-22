import pytest

from nlca_pipelines.validation.values import Spuddate


@pytest.mark.parametrize(
    "spuddate, expected",
    [
        pytest.param("2023-07-01", "2023-07-01", id="valid-date"),
        pytest.param("", None, id="missing-date"),
        pytest.param("2033-01-01", None, id="future-date"),
    ],
)
def test_spuddate(spuddate: str, expected: str) -> None:
    """Test `Spuddate` validator object."""
    assert Spuddate(spuddate=spuddate).spuddate == expected
