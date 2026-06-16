import json

from app.services import candidate_service
from app.services.candidate_service import find_valid_substitute_candidates


def test_find_valid_substitute_candidates_filters_rejected_products():
    candidates = find_valid_substitute_candidates("ENCJK")

    assert len(candidates) == 1
    assert candidates[0].part_number == "ENCJK"
    assert candidates[0].vendor == "Grainger"
    assert candidates[0].condition == "New"
    assert candidates[0].match_percent == 100


def test_find_valid_substitute_candidates_returns_empty_for_unknown_part():
    candidates = find_valid_substitute_candidates("UNKNOWN")

    assert candidates == []


def test_find_valid_substitute_candidates_requires_exact_part_number(tmp_path, monkeypatch):
    candidates_path = tmp_path / "substitute_candidates.json"
    candidates_path.write_text(
        json.dumps(
            [
                {
                    "original_part_number": "ENCJK",
                    "part_number": "ENCJK-ALT",
                    "manufacturer": "nVent Hoffman",
                    "description": "Similar but not exact part number",
                    "vendor": "Grainger",
                    "match_percent": 95,
                    "stock_status": "In Stock",
                    "condition": "New",
                    "product_link": "https://www.grainger.com/",
                    "specifications": {},
                    "notes": [],
                }
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(candidate_service, "SUBSTITUTE_CANDIDATES_PATH", candidates_path)

    candidates = find_valid_substitute_candidates("ENCJK")

    assert candidates == []
