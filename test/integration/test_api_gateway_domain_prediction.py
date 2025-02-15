import pytest
import requests
from io import BytesIO
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

def test_predict_domain_success(client, mock_requests_post):
    """ Testa la predizione del dominio con una user story valida """

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "domain": "Cardiology"
    }

    mock_requests_post.return_value = mock_response

    data = {
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease."
    }

    response = client.post("/predict/domain", json=data)

    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["domain"] == "Cardiology"

def test_predict_domain_invalid_json(client):
    """ Testa l'errore quando il corpo della richiesta non è un JSON valido """

    response = client.post("/predict/domain", data="invalid data", content_type="text/plain")

    assert response.status_code == 400
    assert response.json["status"] == "failure"
    assert "Request body must be JSON" in response.json["motivation"]

def test_predict_domain_missing_user_story(client):
    """ Testa l'errore quando manca il campo 'user_story' """

    response = client.post("/predict/domain", json={})

    # Stampa la risposta per capire meglio il problema
    print("\nResponse JSON:", response.json)
    print("Status Code:", response.status_code)

    assert response.status_code == 400
    assert response.json["status"] == "failure"
    assert "Missing 'user_story'" in response.json["motivation"]


def test_predict_domain_service_down(client, mock_requests_post):
    """ Testa il comportamento se il microservizio Domain Prediction non risponde """

    mock_requests_post.side_effect = requests.exceptions.ConnectionError

    data = {
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes."
    }

    response = client.post("/predict/domain", json=data)

    assert response.status_code == 500
    assert response.json is not None
    assert response.json["status"] == "failure"
    assert "Domain Prediction Service is unavailable" in response.json["motivation"]

