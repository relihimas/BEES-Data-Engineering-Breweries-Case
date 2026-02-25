from unittest.mock import MagicMock
from app.gold.service import GoldService
from app.core.config import settings


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

    # act
    service.run()

    # assert
    sparktransformer.gold_transform_breweries.assert_called_once()
    repository.truncate.assert_called_once()

    # write_table chamado uma vez
    sparkjdbc.write_table.assert_called_once()
    args, kwargs = sparkjdbc.write_table.call_args

    # 1º arg: df
    assert args[0] is fake_df

    # 2º arg: nome da tabela — usa o settings real
    assert args[1] == settings.gold_table  # deve ser "gold_breweries"

    # mode="overwrite"
    assert kwargs.get("mode") == "overwrite"