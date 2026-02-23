from pydantic import BaseModel, Field
from typing import Optional


class Brewery(BaseModel):
    id: str
    name: str
    brewery_type: Optional[str]
    address_1: Optional[str]
    address_2: Optional[str]
    address_3: Optional[str]
    city: Optional[str]
    state_province: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    phone: Optional[str]
    website_url: Optional[str]
    state: Optional[str]
    street: Optional[str]