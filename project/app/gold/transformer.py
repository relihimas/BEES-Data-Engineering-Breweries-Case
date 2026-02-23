from typing import List
from collections import defaultdict
from app.gold.schema import GoldAggregation


class GoldTransformer:

    @staticmethod
    def aggregate(rows: List[dict]) -> List[GoldAggregation]:
        counter = defaultdict(int)

        for row in rows:
            key = (
                row.get("country"),
                row.get("state"),
                row.get("city"),
                row.get("brewery_type"),
            )
            counter[key] += 1

        result = [
            GoldAggregation(
                country=k[0],
                state=k[1],
                city=k[2],
                brewery_type=k[3],
                brewery_count=v,
            )
            for k, v in counter.items()
        ]

        return result