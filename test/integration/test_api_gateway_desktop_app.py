import pytest
import json
from unittest.mock import MagicMock, patch
from io import BytesIO
import requests

API_GATEWAY_URL = "http://localhost:8080"

@pytest.fixture
def mock_requests_post():
    with patch("requests.post") as mock_post:
        yield mock_post

# Test caricamento file (storiesload)
def test_stories_load_success(mock_requests_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success", "stories": ["Story 1", "Story 2"]}
    mock_requests_post.return_value = mock_response

    files = {'stories': ("test.xlsx", BytesIO(b"fake_excel_data"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    response = requests.post(f"{API_GATEWAY_URL}/storiesload", files=files)

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["stories"]) == 2

# Test predizione dominio
def test_predict_domain_success(mock_requests_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success", "domain": "Cardiology"}
    mock_requests_post.return_value = mock_response

    data = {"user_story": "As a cardiologist, I want to analyze patient data."}
    response = requests.post(f"{API_GATEWAY_URL}/predict/domain", json=data)

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["domain"] == "Cardiology"

# Test predizione task
def test_predict_tasks_success(mock_requests_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success", "tasks": ["classification"], "tasks_features": {"classification": ["age", "gender"]}}
    mock_requests_post.return_value = mock_response

    data = {"user_story": "As a cardiologist, I want to analyze patient data.", "domain": "Cardiology"}
    response = requests.post(f"{API_GATEWAY_URL}/predict/tasks", json=data)

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "classification" in response.json()["tasks"]

# Test generazione report
def test_generate_report_success(mock_requests_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"user_story": "Story 1", "domain": "Cardiology", "tasks": ["classification"]}]
    mock_requests_post.return_value = mock_response

    data = {"user_stories": ["As a doctor, I want to analyze X-rays."]}
    response = requests.post(f"{API_GATEWAY_URL}/generate/report", json=data)

    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["domain"] == "Cardiology"

# Test invio feedback dominio
def test_feedback_domain_success(mock_requests_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success", "message": "Domain feedback received"}
    mock_requests_post.return_value = mock_response

    data = {"user_story": "As an engineer, I want to design fair AI systems.", "predicted_domain": "Engineering", "feedback_value": 5}
    response = requests.post(f"{API_GATEWAY_URL}/feedback/domain", json=data)

    assert response.status_code == 200
    assert response.json()["status"] == "success"

# Test invio feedback task
def test_feedback_tasks_success(mock_requests_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success", "message": "Task feedback received"}
    mock_requests_post.return_value = mock_response

    data = {"user_story": "As a scientist, I want to predict climate changes.", "domain": "Science", "predicted_tasks": ["forecasting"], "feedback_value": 4}
    response = requests.post(f"{API_GATEWAY_URL}/feedback/tasks", json=data)

    assert response.status_code == 200
    assert response.json()["status"] == "success"
