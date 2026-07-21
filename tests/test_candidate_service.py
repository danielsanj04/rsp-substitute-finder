import json

from app.services import candidate_service
from app.services.candidate_service import (
    find_valid_original_stock_options,
    find_valid_substitute_candidates,
)


def test_find_valid_original_stock_options_returns_same_part_stock():
    stock_options = find_valid_original_stock_options("ENCJK")

    assert len(stock_options) == 1
    assert stock_options[0].part_number == "ENCJK"
    assert stock_options[0].vendor == "Grainger"
    assert stock_options[0].condition == "New"
    assert stock_options[0].match_percent == 100


def test_find_valid_substitute_candidates_excludes_same_part_stock():
    candidates = find_valid_substitute_candidates("ENCJK")

    assert candidates == []


def test_find_valid_substitute_candidates_returns_empty_for_unknown_part():
    candidates = find_valid_substitute_candidates("UNKNOWN")

    assert candidates == []


def test_find_valid_substitute_candidates_allows_different_part_number(tmp_path, monkeypatch):
    candidates_path = tmp_path / "substitute_candidates.json"
    candidates_path.write_text(
        json.dumps(
            [
                {
                    "original_part_number": "ENCJK",
                    "part_number": "ENCJK-ALT",
                    "manufacturer": "nVent Hoffman",
                    "description": "Compatible alternate joining kit",
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

    assert len(candidates) == 1
    assert candidates[0].part_number == "ENCJK-ALT"


def test_find_valid_original_stock_options_excludes_different_part_number(tmp_path, monkeypatch):
    candidates_path = tmp_path / "substitute_candidates.json"
    candidates_path.write_text(
        json.dumps(
            [
                {
                    "original_part_number": "ENCJK",
                    "part_number": "ENCJK-ALT",
                    "manufacturer": "nVent Hoffman",
                    "description": "Compatible alternate joining kit",
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

    stock_options = find_valid_original_stock_options("ENCJK")

    assert stock_options == []
