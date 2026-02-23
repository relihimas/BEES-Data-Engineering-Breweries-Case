from pyspark.sql import SparkSession, SQLContext, DataFrame
import pyspark.sql.functions as f
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

@contextmanager
def get_spark():
    spark = (
                SparkSession.builder
                .appName("raw_breweries")
                .master("local[*]")
                .config("spark.jars", "/opt/airflow/jars/postgresql-42.7.3.jar")
                .getOrCreate()
            )