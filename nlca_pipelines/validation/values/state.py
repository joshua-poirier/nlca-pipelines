from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class State(BaseModel):
    """Represents US state the well is located in.

    Attributes:
        state (Optional[str]): US state the well is located in.
    """

    state: Optional[str]

    @field_validator("state")
    @classmethod
    def validate_state(cls, v) -> Optional[str]:
        """Sanitize and validate US state's.

        Args:
            v (str): Raw US state to be santized.

        Returns:
            Optional[str]: Sanitized and validated US state.
        """

        # pylint: disable=missing-class-docstring
        class StateEnum(Enum):
            TEXAS = "texas"

        # pylint: enable=missing-class-docstring

        # sanitizing input string
        v = v.lower().strip()

        # initialize US state as missing
        state: Optional[str] = None
        try:
            # sanitize valid values
            state = StateEnum(v).value.upper()
        except ValueError:
            pass

        return state
