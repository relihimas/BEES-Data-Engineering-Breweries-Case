# tests/test_bronze_repository.py
from unittest.mock import MagicMock
from contextlib import contextmanager

from app.bronze.repository import BronzeRepository
from app.core.config import settings
import app.bronze.repository as bronze_repository_module


def test_promote_to_bronze(monkeypatch):
    repo = BronzeRepository()

    fake_cursor = MagicMock()
    fake_conn = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor

    @contextmanager
    def fake_get_connection():
        yield fake_conn

    monkeypatch.setattr(
        bronze_repository_module,
        "get_connection",
        fake_get_connection,
    )

    # act
    repo.promote_to_bronze()

    # pega todos os SQLs executados
    calls = [args[0] for args, _ in fake_cursor.execute.call_args_list]

    # deve ter pelo menos 3 execuções (truncate bronze, insert, truncate sim)
    assert len(calls) >= 3

    # TRUNCATE bronze
    assert any(
        "TRUNCATE" in sql.upper() and settings.bronze_table in sql
        for sql in calls
    ), f"Esperava TRUNCATE em {settings.bronze_table}, mas recebi: {calls}"

    # TRUNCATE bronze_simulation
    assert any(
        "TRUNCATE" in sql.upper() and settings.bronze_simulation_table in sql
        for sql in calls
    ), (
        f"Esperava TRUNCATE em {settings.bronze_simulation_table}, "
        f"mas recebi: {calls}"
    )

    # INSERT bronze FROM bronze_simulation
    assert any(
        "INSERT" in sql.upper()
        and "FROM" in sql.upper()
        and settings.bronze_table in sql
        and settings.bronze_simulation_table in sql
        for sql in calls
    ), (
        f"Esperava INSERT de {settings.bronze_simulation_table} para "
        f"{settings.bronze_table}, mas recebi: {calls}"
    )

    fake_conn.commit.assert_called_once()

def test_transform_and_load_sim(monkeypatch, sample_brewery_list):
    repo = BronzeRepository()

    fake_df = MagicMock()

    from app.core import spark_manager as sm
    monkeypatch.setattr(
        sm.SparkTransformer,
        "bronze_transform_breweries",
        MagicMock(return_value=fake_df),
    )
    monkeypatch.setattr(sm.SparkJDBC, "write_table", MagicMock())

    repo.transform_and_load_sim(sample_brewery_list)

    sm.SparkTransformer.bronze_transform_breweries.assert_called_once()
    sm.SparkJDBC.write_table.assert_called_once()