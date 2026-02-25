# tests/test_bronze_repository.py
from unittest.mock import MagicMock
from app.bronze.repository import BronzeRepository
from app.core.config import settings

def test_promote_to_bronze(monkeypatch):
    repo = BronzeRepository()

    fake_cursor = MagicMock()
    fake_conn = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor

    @contextmanager
    def fake_get_connection():
        yield fake_conn

    from contextlib import contextmanager
    import app.core.database as db

    monkeypatch.setattr(db, "get_connection", fake_get_connection)

    repo.promote_to_bronze()

    truncate_sim = f"TRUNCATE TABLE {settings.bronze_simulation_table};"
    truncate_bronze = f"TRUNCATE TABLE {settings.bronze_table};"
    insert_sql = (
        f"INSERT INTO {settings.bronze_table} "
        f"SELECT id, name, brewery_type, address_1, address_2, address_3, street, city, state_province, state, "
        f"postal_code, country, longitude, latitude, phone, website_url "
        f"FROM {settings.bronze_simulation_table};"
    )

    calls = [args[0] for args, _ in fake_cursor.execute.call_args_list]
    assert truncate_bronze in calls
    assert insert_sql in calls
    assert truncate_sim in calls
    fake_conn.commit.assert_called_once()

def test_transform_and_load_sim(monkeypatch, sample_brewery_list):
    repo = BronzeRepository()

    fake_df = MagicMock()

    from app.core import spark_manager as sm
    monkeypatch.setattr(sm.SparkTransformer, "bronze_transform_breweries", MagicMock(return_value=fake_df))
    monkeypatch.setattr(sm.SparkJDBC, "write_table", MagicMock())

    repo.transform_and_load_sim(sample_brewery_list)

    sm.SparkTransformer.bronze_transform_breweries.assert_called_once()
    sm.SparkJDBC.write_table.assert_called_once()