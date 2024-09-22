from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class Direction(BaseModel):
    """Represents direction of the wellbore.

    Attributes:
        direction (Optional[str]): Direction of the wellbore.
    """

    direction: Optional[str]

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, v) -> Optional[str]:
        """Sanitize and validate direction's.

        Args:
            v (str): Raw direction to be santized.

        Returns:
            Optional[str]: Sanitized and validated direction.
        """

        # pylint: disable=missing-class-docstring
        class DirectionEnum(Enum):
            HORIZONTAL = "horizontal"
            VERTICAL = "vertical"

        # pylint: enable=missing-class-docstring

        # sanitizing input string
        v = v.lower().strip()

        # initialize direction as missing
        direction: Optional[str] = None
        try:
            # sanitize valid values
            direction = DirectionEnum(v).value.upper()
        except ValueError:
            pass

        return direction
