import pytest
from types import SimpleNamespace

from app.bronze.http_client import BreweryApiClient
from app.core.exceptions import ApiException
from app.bronze.schemas import Brewery


def make_response(status_code, json_data):
    return SimpleNamespace(
        status_code=status_code,
        json=lambda: json_data,
    )


def test_fetch_all_success(monkeypatch):
    calls = {"pages": []}

    def fake_get(url, timeout=None, params=None):
        # Metadata call
        if "metadata" in url:
            return make_response(200, {"total": 3})
        # Paginated data call
        page = params["page"]
        calls["pages"].append(page)
        if page == 1:
            return make_response(200, [
                {"id": "1", "name": "A", "brewery_type": "micro"},
                {"id": "2", "name": "B", "brewery_type": "micro"},
            ])
        if page == 2:
            return make_response(200, [
                {"id": "3", "name": "C", "brewery_type": "micro"},
            ])
        return make_response(200, [])

    monkeypatch.setattr("app.bronze.http_client.requests.get", fake_get)

    client = BreweryApiClient(timeout=1)
    breweries = client.fetch_all()

    assert len(breweries) == 3
    assert isinstance(breweries[0], Brewery)
    assert calls["pages"] == [1, 2]


def test_fetch_all_metadata_error(monkeypatch):
    def fake_get(url, timeout=None, params=None):
        return make_response(500, {})

    monkeypatch.setattr("app.bronze.http_client.requests.get", fake_get)

    client = BreweryApiClient()

    with pytest.raises(ApiException):
        client.fetch_all()