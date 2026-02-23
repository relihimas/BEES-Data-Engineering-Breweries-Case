from contextlib import contextmanager
import psycopg2
from app.core.config import settings

@contextmanager
def get_connection():
    conn = psycopg2.connect(
        host=settings.postgres_host,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
        port=settings.postgres_port,
    )
    try:
        yield conn
    finally:
        conn.close()