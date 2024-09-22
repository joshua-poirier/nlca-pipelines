import pytest

from nlca_pipelines.validation.values import Welltype


@pytest.mark.parametrize(
    "welltype, expected",
    [
        pytest.param("oil", "OIL", id="lower-case-valid"),
        pytest.param("gas", "GAS", id="lower-case-valid-2"),
        pytest.param("Oil ", "OIL", id="capitalized-valid"),
        pytest.param("OIL", "OIL", id="upper-case-valid"),
        pytest.param("invalid", None, id="invalid-str"),
        pytest.param("", None, id="empty-str"),
    ],
)
def test_welltype(welltype: str, expected: str) -> None:
    """Test `Welltype` validator object."""
    assert Welltype(welltype=welltype).welltype == expected
