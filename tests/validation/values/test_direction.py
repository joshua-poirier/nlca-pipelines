import pytest

from nlca_pipelines.validation.values import Direction


@pytest.mark.parametrize(
    "direction, expected",
    [
        pytest.param("horizontal", "HORIZONTAL", id="lower-case-valid"),
        pytest.param("vertical", "VERTICAL", id="lower-case-valid-2"),
        pytest.param("Horizontal", "HORIZONTAL", id="capitalized-valid"),
        pytest.param("HORIZONTAL", "HORIZONTAL", id="upper-case-valid"),
        pytest.param("invalid", None, id="invalid-str"),
        pytest.param("", None, id="empty-str"),
    ],
)
def test_direction(direction: str, expected: str) -> None:
    """Test `Direction` validator object."""
    assert Direction(direction=direction).direction == expected
