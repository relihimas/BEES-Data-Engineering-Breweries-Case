from app.gold.service import GoldService


class FakeRepo:
    def fetch_from_silver(self):
        return []

    def truncate(self):
        pass

    def insert(self, data):
        self.inserted = True


class FakeTransformer:
    def aggregate(self, rows):
        return []


def test_gold_service_runs():
    service = GoldService(FakeRepo(), FakeTransformer())
    service.run()