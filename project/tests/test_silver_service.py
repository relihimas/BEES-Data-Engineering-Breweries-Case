from unittest.mock import MagicMock
from app.silver.service import SilverService

def test_silver_service_run():
    repository = MagicMock()
    sparktransformer = MagicMock()
    sparkjdbc = MagicMock()

    fake_df = MagicMock()
    sparktransformer.silver_transform_breweries.return_value = fake_df

    service = SilverService(
        repository=repository,
        sparktransformer=sparktransformer,
        sparkjdbc=sparkjdbc,
    )

    service.run()

    sparktransformer.silver_transform_breweries.assert_called_once()
    repository.truncate.assert_called_once()
    repository.write_silver_parquet.assert_called_once_with(fake_df)