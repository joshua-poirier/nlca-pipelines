from typing import Optional, Union

from pydantic import BaseModel, field_validator


class Cum12mgas(BaseModel):
    """Represents cumulative 12 month gas production for the well.

    Attributes:
        cum12mgas (Optional[Union[int, str]]): Cumulative 12 month gas
            production for the well.
    """

    cum12mgas: Optional[Union[int, str]]

    @field_validator("cum12mgas")
    @classmethod
    def validate_cum12mgas(cls, v) -> Optional[Union[int, str]]:
        """Sanitize and validate Cumulative 12 Month Gas Production.

        Args:
            v (str): Cumulative 12 month gas production.

        Returns:
            Optional[str]: Sanitized and validated cumulative 12 month
                gas production.
        """
        return int(v) if v.isnumeric() and int(v) >= 0 else None
