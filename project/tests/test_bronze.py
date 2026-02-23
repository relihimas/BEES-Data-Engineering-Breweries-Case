import pytest
from app.bronze.service import BronzeService

class FakeRepository:
    def __init__(self):
        self.truncated = False
        self.copied = False

    def truncate(self, table):
        self.truncated = True

    def copy_simulation(self, source, target):
        self.copied = True

def test_bronze_run():
    repo = FakeRepository()
    service = BronzeService(repo)

    service.run()

    assert repo.truncated
    assert repo.copied  