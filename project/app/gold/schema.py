from pydantic import BaseModel
from typing import Optional


class GoldAggregation(BaseModel):
    country: Optional[str]
    state: Optional[str]
    city: Optional[str]
    brewery_type: Optional[str]
    brewery_count: int