from typing import Optional, Union

from pydantic import BaseModel, field_validator


class Cum12mwater(BaseModel):
    """Represents cumulative 12 month water production for the well.

    Attributes:
        cum12mwater (Optional[Union[int, str]]): Cumulative 12 month
            water production for the well.
    """

    cum12mwater: Optional[Union[int, str]]

    @field_validator("cum12mwater")
    @classmethod
    def validate_cum12mwater(cls, v) -> Optional[Union[int, str]]:
        """Sanitize and validate Cumulative 12 Month Water Production.

        Args:
            v (str): Cumulative 12 month water production.

        Returns:
            Optional[str]: Sanitized and validated cumulative 12 month
                water production.
        """
        return int(v) if v.isnumeric() and int(v) >= 0 else None
