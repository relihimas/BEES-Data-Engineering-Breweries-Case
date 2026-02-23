from typing import List
from app.core.database import get_connection
from app.core.config import settings
from app.core.exceptions import DatabaseException
from app.silver.schemas import SilverBrewery


class SilverRepository:

    def truncate(self) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"TRUNCATE TABLE {settings.silver_table};")
                conn.commit()
        except Exception as e:
            raise DatabaseException(str(e))

    def fetch_from_bronze(self) -> List[dict]:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"""
                        SELECT name, brewery_type, city, state, country
                        FROM {settings.bronze_table};
                        """
                    )
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            raise DatabaseException(str(e))

    def insert(self, breweries: List[SilverBrewery]) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    for brewery in breweries:
                        cur.execute(
                            f"""
                            INSERT INTO {settings.silver_table}
                            (name, brewery_type, city, state, country)
                            VALUES (%s, %s, %s, %s, %s);
                            """,
                            (
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