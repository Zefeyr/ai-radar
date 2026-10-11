from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Verify that the health check endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "ai-radar"}


def test_list_articles_empty_or_valid():
    """Verify the /articles endpoint returns a list (empty or populated)."""
    response = client.get("/api/v1/articles?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_nonexistent_article_returns_404():
    """Verify querying an invalid article ID returns a 404 response."""
    response = client.get("/api/v1/articles/99999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Article not found"
