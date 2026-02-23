from app.gold.transformer import GoldTransformer


def test_gold_aggregation():
    raw = [
        {"country": "USA", "state": "CA", "city": "LA", "brewery_type": "Micro"},
        {"country": "USA", "state": "CA", "city": "LA", "brewery_type": "Micro"},
        {"country": "USA", "state": "NY", "city": "NYC", "brewery_type": "Brewpub"},
    ]

    result = GoldTransformer.aggregate(raw)

    assert len(result) == 2

    counts = { (r.country, r.state): r.brewery_count for r in result }

    assert counts[("USA", "CA")] == 2
    assert counts[("USA", "NY")] == 1