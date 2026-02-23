from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import pyspark.sql.functions as f
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
    
    @staticmethod
    def read_parquet(path: str) -> DataFrame:
        spark = SparkManager.get_session()
        logger.info(f"Reading parquet from {path}")
        return spark.read.parquet(path)

class SparkTransformer:

    @staticmethod
    def bronze_transform_breweries(breweries_list: list) -> DataFrame:
        
        spark = SparkManager.get_session()

        logger.info("Transforming breweries DataFrame")

        schema = StructType([
                    StructField("id", StringType(), True),
                    StructField("name", StringType(), True),
                    StructField("brewery_type", StringType(), True),
                    StructField("address_1", StringType(), True),
                    StructField("address_2", StringType(), True),
                    StructField("address_3", StringType(), True),
                    StructField("city", StringType(), True),
                    StructField("state_province", StringType(), True),
                    StructField("postal_code", StringType(), True),
                    StructField("country", StringType(), True),
                    StructField("longitude", StringType(), True),
                    StructField("latitude", StringType(), True),
                    StructField("phone", StringType(), True),
                    StructField("website_url", StringType(), True),
                    StructField("state", StringType(), True),
                    StructField("street", StringType(), True)
                ])
        
        df = spark.createDataFrame(breweries_list, schema=schema)

        return (
            df.withColumn("latitude", df["latitude"].cast("string"))
              .withColumn("longitude", df["longitude"].cast("string"))
        )
    
    @staticmethod
    def silver_transform_breweries(table: str) -> DataFrame:
        spark = SparkManager.get_session()
        df_silver = SparkJDBC.read_table(table)
        df_silver_transf = df_silver.drop("id", "address_1", "address_2", "address_3", "postal_code", 
                                          "phone", "state_province", "website_url", "longitude", "latitude", "street", "created_at", 
                                          "updated_at", "batch_id")

        df_silver_transf = df_silver_transf.withColumn("country", f.trim(f.col("country"))).withColumn("brewery_type", f.initcap(f.col("brewery_type"))).withColumn("country", f.initcap(f.col("country")))
        
        df_silver_transf = df_silver_transf.dropDuplicates()

        return df_silver_transf
    
    @staticmethod
    def gold_transform_breweries(path: str) -> None:
        
        spark = SparkManager.get_session()

        df_gold = SparkJDBC.read_parquet(path)

        df_gold_transf = df_gold.groupBy("country","state","city","brewery_type").agg(f.count("*").alias("brewery_count")).sort("country","state","city")

        return df_gold_transf