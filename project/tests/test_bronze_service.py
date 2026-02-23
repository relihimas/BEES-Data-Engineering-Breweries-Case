from app.bronze.service import BronzeService
from app.bronze.schemas import Brewery


class FakeApiClient:
    def fetch_all(self):
        return [
            Brewery(id="1", name="A"),
            Brewery(id="2", name="B"),
        ]


class FakeRepository:
    def __init__(self):
        self.received = None
        self.promoted = False

    def transform_and_load_sim(self, breweries):
        self.received = breweries

    def promote_to_bronze(self):
        self.promoted = True


def test_bronze_service_run():
    api = FakeApiClient()
    repo = FakeRepository()

    service = BronzeService(api_client=api, repository=repo)

    service.run()

    assert repo.received is not None
    assert len(repo.received) == 2
    assert repo.promoted is True