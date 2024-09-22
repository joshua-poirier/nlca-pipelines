from typing import Optional, Union

from pydantic import BaseModel, field_validator


class Cum12moil(BaseModel):
    """Represents cumulative 12 month oil production for the well.

    Attributes:
        cum12moil (Optional[Union[int, str]]): Cumulative 12 month oil
            production for the well.
    """

    cum12moil: Optional[Union[int, str]]

    @field_validator("cum12moil")
    @classmethod
    def validate_cum12moil(cls, v) -> Optional[Union[int, str]]:
        """Sanitize and validate Cumulative 12 Month Oil Production.

        Args:
            v (str): Cumulative 12 month oil production.

        Returns:
            Optional[str]: Sanitized and validated cumulative 12 month
                oil production.
        """
        return int(v) if v.isnumeric() and int(v) >= 0 else None
