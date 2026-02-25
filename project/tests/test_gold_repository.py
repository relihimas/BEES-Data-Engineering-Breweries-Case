from unittest.mock import MagicMock
from contextlib import contextmanager

from app.gold.repository import GoldRepository
import app.gold.repository as gold_repository_module
from app.core.config import settings


def test_truncate(monkeypatch):
    repo = GoldRepository()

    fake_cursor = MagicMock()
    fake_conn = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor

    @contextmanager
    def fake_get_connection():
        yield fake_conn

    monkeypatch.setattr(
        gold_repository_module,
        "get_connection",
        fake_get_connection,
    )

    # act
    repo.truncate()

    # pegamos todas as chamadas de execute
    calls = [args[0] for args, _ in fake_cursor.execute.call_args_list]

    # deve ter pelo menos 1 (TRUNCATE)
    assert len(calls) >= 1, f"Nenhum SQL executado. Calls: {calls}"

    # deve existir um TRUNCATE na tabela gold
    assert any(
        "TRUNCATE" in sql.upper() and settings.gold_table in sql
        for sql in calls
    ), f"Esperava TRUNCATE em {settings.gold_table}, mas recebi: {calls}"

    # commit chamado
    fake_conn.commit.assert_called_once()