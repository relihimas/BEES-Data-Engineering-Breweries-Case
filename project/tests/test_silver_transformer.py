from app.silver.transformer import SilverTransformer


def test_transformation_removes_duplicates():
    raw = [
        {"name": "A", "brewery_type": "micro", "city": "X", "state": "Y", "country": "usa"},
        {"name": "A", "brewery_type": "micro", "city": "X", "state": "Y", "country": "usa"},
    ]

    result = SilverTransformer.transform(raw)

    assert len(result) == 1
    assert result[0].brewery_type == "Micro"
    assert result[0].country == "Usa"