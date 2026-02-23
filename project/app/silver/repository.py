from pyspark.sql import DataFrame
from app.core.database import get_connection
from app.core.exceptions import DatabaseException
from app.core.spark_manager import SparkJDBC
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("silver-repository")


class SilverRepository:

    def read_from_bronze(self) -> DataFrame:
        logger.info(f"Loading Bronze table {settings.bronze_table} into Spark")
        return SparkJDBC.read_table(settings.bronze_table)

    def write_silver_parquet(self, df_silver: DataFrame) -> None:
        SparkJDBC.write_parquet_partitioned(
            df=df_silver,
            path=settings.silver_path,
            partitions=["country", "state", "city"],
            mode="overwrite",
        )

    def write_silver_table(self, df_silver: DataFrame) -> None:
        logger.info(f"Overwriting Silver table {settings.silver_table}")
        SparkJDBC.write_table(
            df=df_silver,
            table=settings.silver_table,
            mode="overwrite",
        )
    
    def truncate(self) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"TRUNCATE TABLE {settings.silver_table};")
                conn.commit()
        except Exception as e:
            raise DatabaseException(str(e))
        