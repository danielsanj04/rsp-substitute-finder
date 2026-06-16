from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_substitutes_placeholder_response_for_unknown_product():
    response = client.post(
        "/substitutes",
        json={"part_number": "A20H1608SSLP", "manufacturer": "Hoffman"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["search"]["submitted_part_number"] == "A20H1608SSLP"
    assert body["search"]["submitted_manufacturer"] == "Hoffman"
    assert body["original_part"]["part_number"] == "A20H1608SSLP"
    assert body["substitutes"] == []
    assert body["recommendation_status"] == "no_approved_substitute_found"
    assert body["customer_ready_response"] == body["sales_email_summary"]


def test_substitutes_returns_valid_encjk_candidate():
    response = client.post(
        "/substitutes",
        json={"part_number": "ENCJK", "manufacturer": "nVent Hoffman"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["original_part"]["part_number"] == "ENCJK"
    assert len(body["substitutes"]) == 1
    assert body["substitutes"][0]["vendor"] == "Grainger"
    assert body["substitutes"][0]["condition"] == "New"
    assert body["recommendation_status"] == "matches_found"


def test_api_v1_search_accepts_product_details_only():
    response = client.post(
        "/api/v1/search",
        json={"product_details": "stainless steel enclosure 20 x 16 x 8"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["search"]["submitted_product_details"] == "stainless steel enclosure 20 x 16 x 8"
    assert body["search"]["query_text"] == "stainless steel enclosure 20 x 16 x 8"
    assert body["original_part"]["part_number"] == "UNKNOWN"
    assert body["substitutes"] == []


def test_search_requires_at_least_one_input():
    response = client.post("/api/v1/search", json={})

    assert response.status_code == 422
