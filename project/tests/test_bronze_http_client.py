# tests/test_bronze_http_client.py
import pytest
from unittest.mock import MagicMock
from app.bronze.http_client import BreweryApiClient
from app.core.exceptions import ApiException

def test_fetch_all_success(monkeypatch):
    client = BreweryApiClient(timeout=1)

    def fake_get(url, *args, **kwargs):
        mock_resp = MagicMock()
        if "breweries/meta" in url:
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"total": 3}
        else:
            mock_resp.status_code = 200
            mock_resp.json.return_value = [
                {
                    "id": "1",
                    "name": "Test Brewery",
                    "brewery_type": "micro",
                    "address_1": "Street",
                    "address_2": None,
                    "address_3": None,
                    "city": "Recife",
                    "state_province": None,
                    "postal_code": "50000-000",
                    "country": "Brazil",
                    "longitude": "-34.9",
                    "latitude": "-8.0",
                    "phone": "81999999999",
                    "website_url": "http://test.com",
                    "state": "PE",
                    "street": "Street",
                }
            ]
        return mock_resp

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    breweries = client.fetch_all()
    assert len(breweries) == 1
    assert breweries[0].name == "Test Brewery"

def test_fetch_all_metadata_error(monkeypatch):
    client = BreweryApiClient(timeout=1)

    def fake_get(url, *args, **kwargs):
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        return mock_resp

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(ApiException):
        client.fetch_all()

def test_fetch_all_page_error(monkeypatch):
    client = BreweryApiClient(timeout=1)

    def fake_get(url, *args, **kwargs):
        mock_resp = MagicMock()
        if "breweries/meta" in url:
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"total": 1}
        else:
            mock_resp.status_code = 500
        return mock_resp

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(ApiException):
        client.fetch_all()