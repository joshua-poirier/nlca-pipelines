import pytest

from nlca_pipelines.validation.values import Subbasin


@pytest.mark.parametrize(
    "subbasin, expected",
    [
        pytest.param("midland", "MIDLAND", id="lower-case-valid"),
        pytest.param(
            " Central eagle ford", "CENTRAL EAGLE FORD", id="lower-case-valid-2"
        ),
        pytest.param("MAVERICK basin ", "MAVERICK BASIN", id="capitalized-valid"),
        pytest.param("invalid", None, id="invalid-str"),
        pytest.param("", None, id="empty-str"),
    ],
)
def test_subbasin(subbasin: str, expected: str) -> None:
    """Test `Subbasin` validator object."""
    assert Subbasin(subbasin=subbasin).subbasin == expected
