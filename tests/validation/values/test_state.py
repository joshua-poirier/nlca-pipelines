import pytest

from nlca_pipelines.validation.values import State


@pytest.mark.parametrize(
    "state, expected",
    [
        pytest.param("texas ", "TEXAS", id="lower-case-valid"),
        pytest.param("Texas ", "TEXAS", id="capitalized-valid"),
        pytest.param("  TEXAS ", "TEXAS", id="upper-case-valid"),
        pytest.param("invalid", None, id="invalid-str"),
        pytest.param("", None, id="empty-str"),
    ],
)
def test_state(state: str, expected: str) -> None:
    """Test `Subbasin` validator object."""
    assert State(state=state).state == expected
