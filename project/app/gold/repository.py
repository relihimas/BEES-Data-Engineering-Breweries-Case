from typing import List
from app.core.database import get_connection
from app.core.config import settings
from app.core.exceptions import DatabaseException
from app.gold.schema import GoldAggregation


class GoldRepository:

    def truncate(self) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"TRUNCATE TABLE {settings.gold_table};")
                conn.commit()
        except Exception as e:
            raise DatabaseException(str(e))

    def fetch_from_silver(self) -> List[dict]:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"""
                        SELECT country, state, city, brewery_type
                        FROM {settings.silver_table};
                        """
                    )
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            raise DatabaseException(str(e))

    def insert(self, aggregations: List[GoldAggregation]) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    for row in aggregations:
                        cur.execute(
                            f"""
                            INSERT INTO {settings.gold_table}
                            (country, state, city, brewery_type, brewery_count)
                            VALUES (%s, %s, %s, %s, %s);
                            """,
                            (
                                row.country,
                                row.state,
                                row.city,
                                row.brewery_type,
                                row.brewery_count,
                            ),
                        )
                conn.commit()
        except Exception as e:
            raise DatabaseException(str(e))