import pytest

from nlca_pipelines.validation.values import County


@pytest.mark.parametrize(
    "county, expected",
    [
        pytest.param("pecos ", "PECOS", id="lower-case-valid"),
        pytest.param("Anderson ", "ANDERSON", id="capitalized-valid"),
        pytest.param("  COOKE ", "COOKE", id="upper-case-valid"),
        pytest.param("invalid", None, id="invalid-str"),
        pytest.param("", None, id="empty-str"),
    ],
)
def test_county(county: str, expected: str) -> None:
    """Test `County` validator object."""
    assert County(county=county).county == expected
