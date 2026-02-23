from pyspark.sql import SparkSession, DataFrame
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("spark-core")


class SparkManager:

    _spark: SparkSession | None = None

    @classmethod
    def get_session(cls) -> SparkSession:
        if cls._spark is None:
            logger.info("Creating new Spark session")

            cls._spark = (
                SparkSession.builder
                .appName(settings.spark_app_name)
                .master(settings.spark_master)
                .config("spark.jars", settings.spark_postgres_jar)
                .config("spark.sql.adaptive.enabled", "true")
                .config("spark.sql.shuffle.partitions", "200")
                .getOrCreate()
            )

        return cls._spark

    @classmethod
    def stop_session(cls):
        if cls._spark:
            logger.info("Stopping Spark session")
            cls._spark.stop()
            cls._spark = None


class SparkJDBC:

    @staticmethod
    def read_table(table: str) -> DataFrame:
        spark = SparkManager.get_session()

        logger.info(f"Reading table {table} via JDBC")

        return spark.read.jdbc(
            url=settings.postgres_url,
            table=table,
            properties={
                "user": settings.postgres_user,
                "password": settings.postgres_password,
                "driver": "org.postgresql.Driver",
            }
        )

    @staticmethod
    def write_table(df: DataFrame, table: str, mode: str = "append") -> None:
        logger.info(f"Writing DataFrame to {table} via JDBC")

        df.write.jdbc(
            url=settings.postgres_url,
            table=table,
            mode=mode,
            properties={
                "user": settings.postgres_user,
                "password": settings.postgres_password,
                "driver": "org.postgresql.Driver",
            }
        )

    @staticmethod
    def write_parquet_partitioned(
        df: DataFrame,
        path: str,
        partitions: list[str],
        mode: str = "overwrite",
    ) -> None:
        logger.info(f"Writing parquet to {path} partitioned by {partitions}")

        (
            df.write
            .format("parquet")
            .mode(mode)
            .partitionBy(*partitions)
            .option("compression", "snappy")
            .save(path)
        )