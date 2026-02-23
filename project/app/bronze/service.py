from app.bronze.http_client import BreweryApiClient
from app.bronze.repository import BronzeRepository
from app.core.logging import get_logger

logger = get_logger("bronze-service")


class BronzeService:

    def __init__(
        self,
        api_client: BreweryApiClient,
        repository: BronzeRepository,
    ):
        self.api_client = api_client
        self.repository = repository

    def run(self) -> None:
        logger.info("Bronze pipeline started")

        breweries = self.api_client.fetch_all()
        
        logger.info(f"Fetched {len(breweries)} breweries")

        self.repository.transform_and_load_sim(breweries)

        logger.info("Data loaded into bronze simulation table")

        self.repository.promote_to_bronze()

        logger.info("Bronze pipeline completed successfully")