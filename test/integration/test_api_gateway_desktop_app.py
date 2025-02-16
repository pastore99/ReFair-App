import pytest
import requests
import json
from io import BytesIO

# URL del Gateway API in ascolto sulla porta 8080
API_GATEWAY_URL = "http://localhost:8080"

# **Test: Caricamento file (storiesload)**
def test_stories_load_success():
    """Verifica il caricamento di un file Excel e la ricezione delle user stories"""
    files = {
        'stories': ("test.xlsx", BytesIO(b"fake_excel_data"),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }
    response = requests.post(f"{API_GATEWAY_URL}/storiesload", files=files)

    assert response.status_code == 200, f"Errore: {response.text}"
    json_response = response.json()
    assert json_response["status"] == "success"
    assert isinstance(json_response["stories"], list)
    assert len(json_response["stories"]) > 0

# **Test: Predizione dominio**
def test_predict_domain_success():
    """Verifica che una user story venga classificata nel dominio corretto"""
    data = {"user_story": "As a cardiologist, I want to analyze patient data."}
    response = requests.post(f"{API_GATEWAY_URL}/predict/domain", json=data)

    assert response.status_code == 200, f"Errore: {response.text}"
    json_response = response.json()
    assert json_response["status"] == "success"
    assert "domain" in json_response

# **Test: Predizione task**
def test_predict_tasks_success():
    """Verifica la classificazione dei task relativi a una user story"""
    data = {
        "user_story": "As a cardiologist, I want to analyze patient data.",
        "domain": "Cardiology"
    }
    response = requests.post(f"{API_GATEWAY_URL}/predict/tasks", json=data)

    assert response.status_code == 200, f"Errore: {response.text}"
    json_response = response.json()
    assert json_response["status"] == "success"
    assert "tasks" in json_response
    assert isinstance(json_response["tasks"], list)
    assert len(json_response["tasks"]) > 0

# **Test: Generazione report**
def test_generate_report_success():
    """Verifica che il report venga generato correttamente per una lista di user stories"""
    data = {"user_stories": ["As a doctor, I want to analyze X-rays."]}
    response = requests.post(f"{API_GATEWAY_URL}/generate/report", json=data)

    assert response.status_code == 200, f"Errore: {response.text}"
    json_response = response.json()
    assert isinstance(json_response, list)
    assert len(json_response) > 0
    assert "domain" in json_response[0]

# **Test: Invio feedback dominio**
def test_feedback_domain_success():
    """Verifica l'invio di feedback per la predizione del dominio"""
    data = {
        "user_story": "As an engineer, I want to design fair AI systems.",
        "predicted_domain": "Engineering",
        "feedback_value": 5
    }
    response = requests.post(f"{API_GATEWAY_URL}/feedback/domain", json=data)

    assert response.status_code == 200, f"Errore: {response.text}"
    json_response = response.json()
    assert json_response["status"] == "success"

# **Test: Invio feedback task**
def test_feedback_tasks_success():
    """Verifica l'invio del feedback per la predizione dei task associati"""
    data = {
        "user_story": "As a scientist, I want to predict climate changes.",
        "domain": "Science",
        "predicted_tasks": ["forecasting"],
        "feedback_value": 4
    }
    response = requests.post(f"{API_GATEWAY_URL}/feedback/tasks", json=data)

    assert response.status_code == 200, f"Errore: {response.text}"
    json_response = response.json()
    assert json_response["status"] == "success"
