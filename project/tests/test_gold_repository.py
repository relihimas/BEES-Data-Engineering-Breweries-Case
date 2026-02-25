from unittest.mock import MagicMock
from contextlib import contextmanager
from app.gold.repository import GoldRepository
from app.core.config import settings

def test_truncate(monkeypatch):
    repo = GoldRepository()

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