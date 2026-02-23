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