from app.silver.repository import SilverRepository
from app.core.spark_manager import SparkJDBC, SparkTransformer
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("silver-service")


class SilverService:

    def __init__(
        self,
        repository: SilverRepository,
        sparktransformer: SparkTransformer,
        sparkjdbc: SparkJDBC
    ):
        self.repository = repository
        self.sparktransformer = sparktransformer
        self.sparkjdbc = sparkjdbc

    def run(self) -> None:
        logger.info("Silver pipeline started")

        transformed = self.sparktransformer.silver_transform_breweries(settings.bronze_table)
        logger.info(f"Transformed {transformed.count()} records")

        self.repository.truncate()
        self.repository.write_silver_parquet(transformed)

        logger.info("Silver pipeline completed successfully")