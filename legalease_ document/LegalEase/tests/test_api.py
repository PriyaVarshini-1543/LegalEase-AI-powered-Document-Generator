from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["app"] == "LegalEase"


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_document():
    response = client.post(
        "/api/documents/generate",
        json={
            "document_type": "Affidavit",
            "client_name": "Priya",
            "jurisdiction": "India",
            "facts": "The applicant states that the supplied facts are true and accurate.",
            "tone": "Formal",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Affidavit"
    assert len(body["content"]) > 50
    assert body["source"] in {"local", "openai"}
