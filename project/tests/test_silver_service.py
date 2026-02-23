from app.silver.service import SilverService


class FakeRepo:
    def fetch_from_bronze(self):
        return []

    def truncate(self):
        pass

    def insert(self, data):
        self.inserted = True


class FakeTransformer:
    def transform(self, raw):
        return []


def test_silver_service_runs():
    service = SilverService(FakeRepo(), FakeTransformer())
    service.run()