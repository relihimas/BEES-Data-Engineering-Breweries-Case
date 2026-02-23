from app.bronze.service import BronzeService


class FakeApi:
    def fetch_all(self):
        return []


class FakeRepo:
    def truncate_simulation(self): pass
    def insert_simulation(self, breweries): pass
    def promote_to_bronze(self): pass


def test_bronze_service_runs():
    service = BronzeService(FakeApi(), FakeRepo())
    service.run()