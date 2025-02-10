import pytest
import requests
from unittest.mock import MagicMock
from server.api_gateway.api_gateway import app

@pytest.fixture
def client():
    """ Crea un client di test per l'API Gateway """
    app.config["TESTING"] = True
    return app.test_client()

@pytest.fixture
def mock_requests_post(mocker):
    """ Mock per simulare richieste a servizi esterni """
    return mocker.patch("requests.post")

def test_generate_report_success(client, mock_requests_post):
    """ Testa la generazione del report con user stories valide """

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"""
    [
        {
            "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
            "domain": "Cardiology",
            "tasks": ["classification", "ranking"],
            "tasks_features": {
                "classification": ["race", "age", "sex"],
                "ranking": ["race", "age", "sex"]
            }
        }
    ]
    """

    mock_requests_post.return_value = mock_response

    data = {
        "user_stories": [
            "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease."
        ]
    }

    response = client.post("/generate/report", json=data)

    assert response.status_code == 200
    assert response.data is not None
    assert b'"user_story"' in response.data  # Controlla che ci sia almeno una user story nel JSON

def test_generate_report_invalid_json(client):
    """ Testa l'errore quando il corpo della richiesta non è un JSON valido """

    response = client.post("/generate/report", data="invalid data", content_type="text/plain")

    assert response.status_code == 400
    assert response.json["status"] == "failure"
    assert "Request body must be JSON" in response.json["motivation"]

def test_generate_report_missing_user_stories(client):
    """ Testa l'errore quando manca il campo 'user_stories' """

    response = client.post("/generate/report", json={})

    assert response.status_code == 500

def test_generate_report_service_down(client, mock_requests_post):
    """ Testa il comportamento se il microservizio Report Generation non risponde """

    mock_requests_post.side_effect = requests.exceptions.ConnectionError

    data = {
        "user_stories": [
            "As a cardiologist, I want to identify multiword expressions in patient notes."
        ]
    }

    response = client.post("/generate/report", json=data)

    assert response.status_code == 500
    assert response.json is not None
    assert response.json["status"] == "failure"
    assert "Report Generation Service is unavailable" in response.json["motivation"]
