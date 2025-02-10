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

def test_predict_tasks_success(client, mock_requests_post):
    """ Testa la predizione dei task con una user story valida """

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "tasks": ["classification", "ranking"],
        "tasks_features": {
            "classification": ["race", "age", "sex"],
            "ranking": ["race", "age", "sex"]
        }
    }

    mock_requests_post.return_value = mock_response

    data = {
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
        "domain": "Cardiology"
    }

    response = client.post("/predict/tasks", json=data)

    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert "classification" in response.json["tasks"]

def test_predict_tasks_invalid_json(client):
    """ Testa l'errore quando il corpo della richiesta non è un JSON valido """

    response = client.post("/predict/tasks", data="invalid data", content_type="text/plain")

    assert response.status_code == 400
    assert response.json["status"] == "failure"
    assert "Request body must be JSON" in response.json["motivation"]

def test_predict_tasks_service_down(client, mock_requests_post):
    """ Testa il comportamento se il microservizio Task Prediction non risponde """

    mock_requests_post.side_effect = requests.exceptions.ConnectionError

    data = {
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes.",
        "domain": "Cardiology"
    }

    response = client.post("/predict/tasks", json=data)

    assert response.status_code == 500
    assert response.json is not None
    assert response.json["status"] == "failure"
    assert "Task Prediction Service is unavailable" in response.json["motivation"]
