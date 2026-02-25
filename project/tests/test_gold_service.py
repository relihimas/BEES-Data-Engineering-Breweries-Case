from unittest.mock import MagicMock
from app.gold.service import GoldService

def test_gold_service_run():
    repository = MagicMock()
    sparktransformer = MagicMock()
    sparkjdbc = MagicMock()

    fake_df = MagicMock()
    sparktransformer.gold_transform_breweries.return_value = fake_df

    service = GoldService(
        repository=repository,
        sparktransformer=sparktransformer,
        sparkjdbc=sparkjdbc,
    )

    service.run()

    sparktransformer.gold_transform_breweries.assert_called_once()
    repository.truncate.assert_called_once()
    sparkjdbc.write_table.assert_called_once_with(fake_df, service.sparkjdbc.settings.gold_table, mode="overwrite")