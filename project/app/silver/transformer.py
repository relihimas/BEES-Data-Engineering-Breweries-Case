from typing import List
from app.silver.schemas import SilverBrewery


class SilverTransformer:

    @staticmethod
    def transform(raw_rows: List[dict]) -> List[SilverBrewery]:
        transformed = []

        for row in raw_rows:
            brewery = SilverBrewery(
                name=row["name"],
                brewery_type=(row["brewery_type"] or "").title(),
                city=row["city"],
                state=row["state"],
                country=(row["country"] or "").title(),
            )

            transformed.append(brewery)

        # Remove duplicados
        unique = {b.model_dump_json(): b for b in transformed}

        return list(unique.values())