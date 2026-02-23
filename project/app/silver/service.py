from app.silver.repository import SilverRepository
from app.silver.transformer import SilverTransformer
from app.core.logging import get_logger

logger = get_logger("silver-service")


class SilverService:

    def __init__(
        self,
        repository: SilverRepository,
        transformer: SilverTransformer,
    ):
        self.repository = repository
        self.transformer = transformer

    def run(self) -> None:
        logger.info("Silver pipeline started")

        raw_data = self.repository.fetch_from_bronze()
        logger.info(f"Fetched {len(raw_data)} records from Bronze")

        transformed = self.transformer.transform(raw_data)
        logger.info(f"{len(transformed)} records after transformation")

        self.repository.truncate()
        self.repository.insert(transformed)

        logger.info("Silver pipeline completed successfully")