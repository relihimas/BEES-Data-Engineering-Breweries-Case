from pydantic import BaseModel
from typing import Optional


class SilverBrewery(BaseModel):
    name: str
    brewery_type: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]