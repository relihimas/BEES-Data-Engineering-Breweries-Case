from app.silver.service import SilverService
from app.silver.repository import SilverRepository
from app.silver.transformer import SilverTransformer


def run_silver():
    service = SilverService(
        repository=SilverRepository(),
        transformer=SilverTransformer(),
    )
    service.run()


if __name__ == "__main__":
    run_silver()