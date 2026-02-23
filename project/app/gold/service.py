from app.gold.repository import GoldRepository
from app.gold.transformer import GoldTransformer
from app.core.logging import get_logger

logger = get_logger("gold-service")


class GoldService:

    def __init__(
        self,
        repository: GoldRepository,
        transformer: GoldTransformer,
    ):
        self.repository = repository
        self.transformer = transformer

    def run(self) -> None:
        logger.info("Gold pipeline started")

        rows = self.repository.fetch_from_silver()
        logger.info(f"Fetched {len(rows)} records from Silver")

        aggregated = self.transformer.aggregate(rows)
        logger.info(f"{len(aggregated)} aggregated rows generated")

        self.repository.truncate()
        self.repository.insert(aggregated)

        logger.info("Gold pipeline completed successfully")