
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_endpoint():
    r = client.post("/analyze", json={"text": "Test the API. It extracts nouns and topics."})
    assert r.status_code == 200
    data = r.json()
    assert "summary" in data and data["summary"]
    assert "keywords" in data and isinstance(data["keywords"], list)

def test_empty_text_rejected():
    r = client.post("/analyze", json={"text": "   "})
    assert r.status_code == 400
    assert r.json()["detail"] == "text must not be empty"

def test_search_endpoint():
    client.post("/analyze", json={"text": "Apples and oranges. Fruits market analysis."})
    r = client.get("/search", params={"topic":"fruits"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)
