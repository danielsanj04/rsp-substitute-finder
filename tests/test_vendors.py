from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_approved_vendors_endpoint_returns_vendor_list():
    response = client.get("/api/v1/vendors/approved")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == len(body["vendors"])
    assert "Grainger" in body["vendors"]
