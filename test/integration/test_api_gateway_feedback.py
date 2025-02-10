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

def test_feedback_domain_success(client, mock_requests_post):
    """ Testa l'invio di un feedback valido per il dominio """

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "message": "Domain feedback received"
    }

    mock_requests_post.return_value = mock_response

    data = {
        "user_story": "As an orthopedic surgeon, I want to review X-ray images to identify bone fractures quickly.",
        "predicted_domain": "orthopedics",
        "feedback_value": 4
    }

    response = client.post("/feedback/domain", json=data)

    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["message"] == "Domain feedback received"

def test_feedback_tasks_success(client, mock_requests_post):
    """ Testa l'invio di un feedback valido per i task """

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "message": "Task feedback received"
    }

    mock_requests_post.return_value = mock_response

    data = {
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
        "domain": "cardiology",
        "predicted_tasks": ["Identify Multiword Expressions", "Risk Factor Analysis"],
        "feedback_value": 5
    }

    response = client.post("/feedback/tasks", json=data)

    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["message"] == "Task feedback received"

def test_feedback_invalid_json(client):
    """ Testa l'errore quando il corpo della richiesta non è un JSON valido """

    response = client.post("/feedback/domain", data="invalid data", content_type="text/plain")

    assert response.status_code == 400
    assert response.json["status"] == "failure"
    assert "Request body must be JSON" in response.json["motivation"]

def test_feedback_service_down(client, mock_requests_post):
    """ Testa il comportamento se il microservizio Feedback non risponde """

    mock_requests_post.side_effect = requests.exceptions.ConnectionError

    data = {
        "user_story": "As an orthopedic surgeon, I want to review X-ray images to identify bone fractures quickly.",
        "predicted_domain": "orthopedics",
        "feedback_value": 4
    }

    response = client.post("/feedback/domain", json=data)

    assert response.status_code == 500
    assert response.json is not None
    assert response.json["status"] == "failure"
    assert "Feedback Service is unavailable" in response.json["motivation"]
