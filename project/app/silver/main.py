from app.silver.service import SilverService
from app.silver.repository import SilverRepository

def run_silver():
    service = SilverService(
        repository=SilverRepository()
    )
    service.run()


if __name__ == "__main__":
    run_silver()