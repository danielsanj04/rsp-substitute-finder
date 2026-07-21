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
    assert body["original_stock_options"] == []
    assert body["substitute_options"] == []
    assert body["recommendation_status"] == "no_approved_substitute_found"
    assert body["customer_ready_response"] == body["sales_email_summary"]


def test_substitutes_classifies_same_part_match_as_original_stock_not_substitute():
    response = client.post(
        "/substitutes",
        json={"part_number": "ENCJK", "manufacturer": "nVent Hoffman"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["original_part"]["part_number"] == "ENCJK"
    assert len(body["original_stock_options"]) == 1
    assert body["original_stock_options"][0]["part_number"] == "ENCJK"
    assert body["original_stock_options"][0]["vendor"] == "Grainger"
    assert body["original_stock_options"][0]["condition"] == "New"
    assert body["substitute_options"] == []
    assert body["substitutes"] == []
    assert body["recommendation_status"] == "original_stock_found"


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
    assert body["original_stock_options"] == []
    assert body["substitute_options"] == []


def test_api_v1_search_parses_brand_part_and_keywords_from_freeform_query():
    response = client.post(
        "/api/v1/search",
        json={"product_details": "hoffman enclosure CSD24168"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["search"]["parsed_part_number"] == "CSD24168"
    assert body["search"]["parsed_manufacturer"] == "nVent Hoffman"
    assert body["search"]["parsed_keywords"] == ["enclosure"]
    assert body["original_part"]["part_number"] == "CSD24168"
    assert body["original_part"]["manufacturer"] == "nVent Hoffman"


def test_api_v1_search_ignores_bad_first_token_part_number_when_details_are_parseable():
    response = client.post(
        "/api/v1/search",
        json={"part_number": "nVent", "product_details": "nVent Hoffman CSD24168"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["search"]["submitted_part_number"] == "nVent"
    assert body["search"]["parsed_part_number"] == "CSD24168"
    assert body["search"]["parsed_manufacturer"] == "nVent Hoffman"
    assert body["original_part"]["part_number"] == "CSD24168"


def test_search_requires_at_least_one_input():
    response = client.post("/api/v1/search", json={})

    assert response.status_code == 422
