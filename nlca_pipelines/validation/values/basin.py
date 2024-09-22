from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class Basin(BaseModel):
    """Represents the basin the well is located.

    Attributes:
        basin (Optional[str]): Basin the well is located in.
    """

    basin: Optional[str]

    @field_validator("basin")
    @classmethod
    def validate_basin(cls, v) -> Optional[str]:
        """Sanitize and validate basin's.

        Args:
            v (str): Raw basin to be sanitized.

        Returns:
            Optional[str]: Sanitized and validated basin.
        """

        # pylint: disable=missing-class-docstring
        class BasinEnum(Enum):
            ANADARKO = "anadarko"
            BARNETT = "barnett"
            EAGLEFORD = "eagle ford"
            OTHER = "other"
            PERMIAN = "permian"
        # pylint: enable=missing-class-docstring

        # sanitizing input string
        v = v.lower().strip()

        # initialize basin as missing
        basin: Optional[str] = None
        try:
            # sanitize valid values
            basin = BasinEnum(v).name
        except ValueError:
            pass

        return basin
