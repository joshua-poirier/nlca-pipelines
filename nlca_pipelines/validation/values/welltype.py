from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class Welltype(BaseModel):
    """Represents the type of well.

    Attributes:
        welltype (Optional[str]): Type of the well.
    """

    welltype: Optional[str]

    @field_validator("welltype")
    @classmethod
    def validate_welltype(cls, v) -> Optional[str]:
        """Sanitize and validate well type's.

        Args:
            v (str): Raw well type to be sanitized.

        Returns:
            Optional[str]: Sanitized and validated well type.
        """

        # pylint: disable=missing-class-docstring
        class WelltypeEnum(Enum):
            GAS = "gas"
            OIL = "oil"

        # pylint: enable=missing-class-docstring

        # sanitizing input string
        v = v.lower().strip()

        # initialize well type as missing
        welltype: Optional[str] = None
        try:
            # sanitize valid values
            welltype = WelltypeEnum(v).value.upper()
        except ValueError:
            pass

        return welltype
