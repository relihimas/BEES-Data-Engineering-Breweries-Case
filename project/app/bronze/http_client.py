import requests
import math
from typing import List
from app.core.config import settings
from app.core.exceptions import ApiException
from app.bronze.schemas import Brewery

class BreweryApiClient:

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def fetch_all(self) -> List[Brewery]:
        metadata = requests.get(settings.metadata_url, timeout=self.timeout)

        if metadata.status_code != 200:
            raise ApiException("Failed to fetch metadata")

        total = metadata.json()["total"]
        pages = math.ceil(total / 200)

        breweries: List[Brewery] = []

        for page in range(1, pages + 1):
            response = requests.get(
                settings.breweries_url,
                params={"page": page, "per_page": 200},
                timeout=self.timeout,
            )

            if response.status_code != 200:
                raise ApiException(f"Failed at page {page}")

            breweries.extend(
                Brewery(**item) for item in response.json()
            )

        return breweries