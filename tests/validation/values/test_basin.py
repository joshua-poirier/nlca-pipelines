import pytest

from nlca_pipelines.validation.values import Basin


@pytest.mark.parametrize(
    "basin, expected",
    [
        pytest.param("anadarko", "ANADARKO", id="lower-case-valid"),
        pytest.param("barnett", "BARNETT", id="lower-case-valid-2"),
        pytest.param("Eagle ford", "EAGLE FORD", id="capitalized-valid"),
        pytest.param("OTHER", "OTHER", id="upper-case-valid"),
        pytest.param("invalid", None, id="invalid-str"),
        pytest.param("", None, id="empty-str"),
    ],
)
def test_basin(basin: str, expected: str) -> None:
    """Test `Basin` validator object."""
    assert Basin(basin=basin).basin == expected
