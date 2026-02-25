# tests/test_bronze_service.py
from unittest.mock import MagicMock
from app.bronze.service import BronzeService

def test_bronze_service_run():
    api_client = MagicMock()
    repository = MagicMock()

    api_client.fetch_all.return_value = ["brew1", "brew2"]

    service = BronzeService(api_client=api_client, repository=repository)
    service.run()

    api_client.fetch_all.assert_called_once()
    repository.transform_and_load_sim.assert_called_once_with(["brew1", "brew2"])
    repository.promote_to_bronze.assert_called_once()