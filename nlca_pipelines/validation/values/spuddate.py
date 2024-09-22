from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class Spuddate(BaseModel):
    """Represents the spud date of the well.

    Attributes:
        spuddate (Optional[str]): Spud date of the well.
    """

    spuddate: Optional[str]

    @field_validator("spuddate")
    @classmethod
    def validate_spuddate(cls, v) -> Optional[str]:
        """Sanitize and validate Spud Date's.

        Args:
            v (str): Raw spud date to be sanitized.

        Returns:
            Optional[str]: Sanitized and validated Spud Date.
        """
        # initialize Spud Date as missing
        spuddate: Optional[str] = None
        try:
            # parse datetime from string representation of spuddate
            d: datetime = datetime.strptime(v, "%Y-%m-%d")

            # spuddates must be in the past
            spuddate = d.strftime("%Y-%m-%d") if d <= datetime.now() else None
        except ValueError:
            pass

        return spuddate
