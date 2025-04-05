import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_get_version():
    """Teste le endpoint GET /version."""
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()
    assert response.json()["version"] == "1.0.0"

def test_get_prediction_by_date_valid():
    """Teste le endpoint GET /date/{date} pour une date valide."""
    date = "2025-03-25 00:00"
    response = client.get(f"/date/{date}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_prediction_by_date_invalid():
    """Teste le endpoint GET /date/{date} pour une date invalide."""
    date = "2025-03-26"
    response = client.get(f"/date/{date}X")
    assert response.status_code == 404
    assert "Erreur lors de la récupération des prédictions pour" in response.json()["detail"]

def test_get_all_predictions():
    """Teste le endpoint GET /predictions."""
    response = client.get("/predictions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
