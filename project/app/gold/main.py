from app.gold.service import GoldService
from app.gold.repository import GoldRepository


def run_gold():
    service = GoldService(
        repository=GoldRepository()
    )
    service.run()


if __name__ == "__main__":
    run_gold()