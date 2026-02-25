from unittest.mock import MagicMock
from contextlib import contextmanager
from app.silver.repository import SilverRepository
from app.core.config import settings

def test_read_from_bronze(monkeypatch):
    repo = SilverRepository()
    fake_df = MagicMock()

    from app.core import spark_manager as sm
    monkeypatch.setattr(sm.SparkJDBC, "read_table", MagicMock(return_value=fake_df))

    result = repo.read_from_bronze()
    sm.SparkJDBC.read_table.assert_called_once_with(settings.bronze_table)
    assert result is fake_df

def test_write_silver_parquet(monkeypatch):
    repo = SilverRepository()
    fake_df = MagicMock()

    from app.core import spark_manager as sm
    monkeypatch.setattr(sm.SparkJDBC, "write_parquet_partitioned", MagicMock())

    repo.write_silver_parquet(fake_df)
    sm.SparkJDBC.write_parquet_partitioned.assert_called_once()

def test_write_silver_table(monkeypatch):
    repo = SilverRepository()
    fake_df = MagicMock()

    from app.core import spark_manager as sm
    monkeypatch.setattr(sm.SparkJDBC, "write_table", MagicMock())

    repo.write_silver_table(fake_df)
    sm.SparkJDBC.write_table.assert_called_once()

def test_truncate(monkeypatch):
    repo = SilverRepository()

    fake_cursor = MagicMock()
    fake_conn = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor

    @contextmanager
    def fake_get_connection():
        yield fake_conn

    import app.core.database as db
    monkeypatch.setattr(db, "get_connection", fake_get_connection)

    repo.truncate()

    fake_cursor.execute.assert_called_once()
    fake_conn.commit.assert_called_once()