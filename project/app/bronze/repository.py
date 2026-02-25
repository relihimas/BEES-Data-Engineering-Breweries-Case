from typing import List
from app.core.database import get_connection
from app.core.config import settings
from app.core.exceptions import DatabaseException
from app.bronze.schemas import Brewery
from app.core.spark_manager import SparkJDBC, SparkTransformer

class BronzeRepository:

    def promote_to_bronze(self):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"TRUNCATE TABLE {settings.bronze_table};")
                    cur.execute(f"INSERT INTO {settings.bronze_table} SELECT id, name, brewery_type, address_1, address_2, address_3, street, city, state_province, state, postal_code, country, longitude, latitude, phone, website_url FROM {settings.bronze_simulation_table};")
                    cur.execute(f"TRUNCATE TABLE {settings.bronze_simulation_table};")
                conn.commit()
        except Exception as e:
            raise DatabaseException(str(e))

    def transform_and_load_sim(self, breweries: List[Brewery]):
        try:
            df_breweries = SparkTransformer.bronze_transform_breweries(breweries)
            SparkJDBC.write_table(df_breweries, 
                                  settings.bronze_simulation_table,
                                  mode="overwrite")
        except Exception as e:
            raise DatabaseException(str(e))                                        
    