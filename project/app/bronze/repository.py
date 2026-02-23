from typing import List
from app.core.database import get_connection
from app.core.config import settings
from app.core.exceptions import DatabaseException
from app.bronze.schemas import Brewery


class BronzeRepository:

    def truncate_simulation(self):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"TRUNCATE TABLE {settings.bronze_simulation_table};")
                conn.commit()
        except Exception as e:
            raise DatabaseException(str(e))

    def insert_simulation(self, breweries: List[Brewery]):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    for brewery in breweries:
                        cur.execute(
                            f"""
                            INSERT INTO {settings.bronze_simulation_table}
                            (id, name, brewery_type, city, state, country)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            (
                                brewery.id,
                                brewery.name,
                                brewery.brewery_type,
                                brewery.city,
                                brewery.state,
                                brewery.country,
                            ),
                        )
                conn.commit()
        except Exception as e:
            raise DatabaseException(str(e))

    def promote_to_bronze(self):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"TRUNCATE TABLE {settings.bronze_table};")
                    cur.execute(
                        f"""
                        INSERT INTO {settings.bronze_table}
                        SELECT * FROM {settings.bronze_simulation_table};
                        """
                    )
                conn.commit()
        except Exception as e:
            raise DatabaseException(str(e))