import pytest
import requests
from unittest.mock import MagicMock
from server.microservices.services.prediction_service import PredictionService

@pytest.fixture
def prediction_service():
    """ Crea un'istanza di PredictionService con URL fittizi """
    return PredictionService(domain_service_url="http://mock-domain", task_service_url="http://mock-task")

def test_get_domain_success(prediction_service, mocker):
    """ Testa la predizione del dominio con successo """

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success", "domain": "Healthcare"}

    mocker.patch("requests.post", return_value=mock_response)

    domain = prediction_service.get_domain("As a doctor, I want to analyze patient data to detect anomalies.")

    assert domain == "Healthcare"

def test_get_domain_failure(prediction_service, mocker):
    """ Testa il caso in cui la predizione del dominio fallisce """

    mock_response = MagicMock()
    mock_response.status_code = 500  # Errore nel microservizio

    mocker.patch("requests.post", return_value=mock_response)

    with pytest.raises(ValueError, match="Failed to predict domain for story"):
        prediction_service.get_domain("As a doctor, I want to analyze patient data to detect anomalies.")

def test_get_tasks_success(prediction_service, mocker):
    """ Testa la predizione delle task con successo """

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "tasks": ["classification", "risk analysis"],
        "tasks_features": {"classification": ["age", "race"], "risk analysis": ["sex", "history"]}
    }

    mocker.patch("requests.post", return_value=mock_response)

    tasks, tasks_features = prediction_service.get_tasks("As a doctor, I want to analyze patient data.", "Healthcare")

    assert tasks == ["classification", "risk analysis"]
    assert "classification" in tasks_features

def test_get_tasks_failure(prediction_service, mocker):
    """ Testa il caso in cui la predizione delle task fallisce """

    mock_response = MagicMock()
    mock_response.status_code = 500  # Errore nel microservizio

    mocker.patch("requests.post", return_value=mock_response)

    with pytest.raises(ValueError, match="Failed to predict tasks for story"):
        prediction_service.get_tasks("As a doctor, I want to analyze patient data.", "Healthcare")
