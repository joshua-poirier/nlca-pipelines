from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class Subbasin(BaseModel):
    """Represents subbasin the well is located in.

    Attributes:
        subbasin (Optional[str]): Subbasin the well is located in.
    """

    subbasin: Optional[str]

    @field_validator("subbasin")
    @classmethod
    def validate_subbasin(cls, v) -> Optional[str]:
        """Sanitize and validate subbasin's.

        Args:
            v (str): Raw subbasin to be sanitized.

        Returns:
            Optional[str]: Sanitized and validated subbasin.
        """

        # pylint: disable=missing-class-docstring
        class SubbasinEnum(Enum):
            BARNETT = "barnett"
            CENTRAL_BASIN_PLATFORM = "central basin platform"
            CENTRAL_EAGLE_FORD = "central eagle ford"
            DELAWARE = "delaware"
            EASTERN_SHELF = "eastern shelf"
            GRANITE_WASH = "granite wash"
            MAVERICK_BASIN = "maverick basin"
            MIDLAND = "midland"
            NORTHEASTERN_EAGLE_FORD = "northeastern eagle ford"
            NORTHWEST_SHELF = "northwest shelf"
            OTHER = "other"
            SCOOP = "scoop"

        # pylint: enable=missing-class-docstring

        # sanitizing input string
        v = v.lower().strip()

        # intiialize subbasin as missing
        subbasin: Optional[str] = None
        try:
            # sanitize valid values
            subbasin = SubbasinEnum(v).value.upper()
        except ValueError:
            pass

        return subbasin
