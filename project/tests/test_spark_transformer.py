# tests/test_spark_transformer.py
import pytest
from app.core.spark_manager import SparkManager, SparkTransformer
from app.bronze.schemas import Brewery

@pytest.fixture(scope="module")
def spark():
    spark = SparkManager.get_session()
    yield spark
    SparkManager.stop_session()

def test_bronze_transform_breweries(spark):
    breweries = [
        {
            "id": "1",
            "name": "Test Brewery",
            "brewery_type": "micro",
            "address_1": "Street 1",
            "address_2": None,
            "address_3": None,
            "city": "Recife",
            "state_province": None,
            "postal_code": "50000-000",
            "country": "brazil",
            "longitude": "-34.9",
            "latitude": "-8.0",
            "phone": "81999999999",
            "website_url": "http://test.com",
            "state": "PE",
            "street": "Street 1",
        }
    ]

    df = SparkTransformer.bronze_transform_breweries(breweries)
    assert df.count() == 1
    assert "longitude" in df.columns
    assert "latitude" in df.columns

def test_gold_transform_breweries(spark, tmp_path):
    # Cria um parquet fake para simular o silver_path
    from pyspark.sql import Row

    rows = [
        Row(country="Brazil", state="PE", city="Recife", brewery_type="Micro"),
        Row(country="Brazil", state="PE", city="Recife", brewery_type="Micro"),
    ]
    df = spark.createDataFrame(rows)
    path = str(tmp_path / "silver_parquet")
    df.write.mode("overwrite").parquet(path)

    df_gold = SparkTransformer.gold_transform_breweries(path)
    result = df_gold.collect()

    assert len(result) == 1
    row = result[0]
    assert row.brewery_count == 2
    assert row.country == "Brazil"
    assert row.city == "Recife"