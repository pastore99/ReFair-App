import pytest
import requests

from server.api_gateway.api_gateway import app
from io import BytesIO
from unittest.mock import MagicMock

@pytest.fixture
def client():
    """ Crea un client di test per l'API Gateway """
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def mock_requests_post(mocker):
    """ Mock per simulare richieste a servizi esterni """
    return mocker.patch("requests.post")

def test_stories_load_success(client, mock_requests_post):
    """ Testa il caricamento di un file valido attraverso API Gateway """

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "stories": ["Story 1", "Story 2"]
    }

    mock_requests_post.return_value = mock_response

    data = {
        "stories": (BytesIO(b"fake_excel_data"), "test.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }

    response = client.post("/storiesload", content_type="multipart/form-data", data=data)

    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert len(response.json["stories"]) == 2

def test_stories_load_no_file(client):
    """ Testa l'errore quando non viene inviato alcun file """

    response = client.post("/storiesload")

    assert response.status_code == 400

def test_stories_load_service_down(client, mock_requests_post):
    """ Testa il comportamento se il microservizio File Management non risponde """

    mock_requests_post.side_effect = requests.exceptions.ConnectionError

    data = {
        "stories": (BytesIO(b"fake_excel_data"), "test.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }

    response = client.post("/storiesload", content_type="multipart/form-data", data=data)

    assert response.status_code == 500
    assert response.json is not None
    assert response.json["status"] == "failure"
    assert "File Management Service is unavailable" in response.json["motivation"]

