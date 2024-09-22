from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class County(BaseModel):
    """Represents US county the well is located in.

    Attributes:
        county (Optional[str]): US county the well is located in.
    """

    county: Optional[str]

    @field_validator("county")
    @classmethod
    def validate_county(cls, v) -> Optional[str]:
        """Sanitize and validate US county's.

        Args:
            v (str): Raw US county to be santized.

        Returns:
            Optional[str]: Sanitized and validated US county.
        """

        # pylint: disable=missing-class-docstring
        class CountyEnum(Enum):
            ANDERSON = "anderson"
            ATASCOSA = "atascosa"
            BORDEN = "borden"
            COOKE = "cooke"
            CRANE = "crane"
            DEWITT = "dewitt"
            KNOX = "knox"
            MARTIN = "martin"
            MATAGORDA = "matagorda"
            NOLAN = "nolan"
            PECOS = "pecos"
            REFUGIO = "refugio"
            ROBERTSON = "robertson"
            RUNNELS = "runnels"
            YOAKUM = "yoakum"
            YOUNG = "young"

        # pylint: enable=missing-class-docstring

        # sanitizing input string
        v = v.lower().strip()

        # initialize US county as missing
        county: Optional[str] = None
        try:
            # sanitize valid values
            county = CountyEnum(v).value.upper()
        except ValueError:
            pass

        return county
