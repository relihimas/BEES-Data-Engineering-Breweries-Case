from app.gold.service import GoldService
from app.gold.repository import GoldRepository
from app.gold.transformer import GoldTransformer


def run_gold():
    service = GoldService(
        repository=GoldRepository(),
        transformer=GoldTransformer(),
    )
    service.run()


if __name__ == "__main__":
    run_gold()