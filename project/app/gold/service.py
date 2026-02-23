from app.gold.repository import GoldRepository
from app.core.spark_manager import SparkJDBC, SparkTransformer
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("gold-service")

class GoldService:

    def __init__(
        self,
        repository: GoldRepository,
        sparktransformer: SparkTransformer,
        sparkjdbc: SparkJDBC
    ):
        self.repository = repository
        self.sparktransformer = sparktransformer
        self.sparkjdbc = sparkjdbc

    def run(self) -> None:
        logger.info("Gold pipeline started")

        aggregated = self.sparktransformer.gold_transform_breweries(settings.silver_path)
        logger.info(f"{len(aggregated)} aggregated rows generated")

        self.repository.truncate()
        self.sparkjdbc.write_table(aggregated, settings.gold_table, mode="overwrite")

        logger.info("Gold pipeline completed successfully")