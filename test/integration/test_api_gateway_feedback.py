import pytest
import requests

API_GATEWAY_URL = "http://localhost:8080"

@pytest.fixture
def client():
    """ Restituisce un client di test per l'API Gateway """
    return requests.Session()

def test_feedback_domain_success(client):
    """ Testa l'invio di un feedback valido per il dominio """

    data = {
        "user_story": "As an orthopedic surgeon, I want to review X-ray images to identify bone fractures quickly.",
        "predicted_domain": "orthopedics",
        "feedback_value": 4
    }

    response = client.post(f"{API_GATEWAY_URL}/feedback/domain", json=data)

    print("Response Status:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 200, f"Errore HTTP: {response.status_code} - {response.text}"
    json_response = response.json()
    assert json_response["status"] == "success"
    assert json_response["message"] == "Domain feedback received"

def test_feedback_tasks_success(client):
    """ Testa l'invio di un feedback valido per i task """

    data = {
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
        "domain": "cardiology",
        "predicted_tasks": ["Identify Multiword Expressions", "Risk Factor Analysis"],
        "feedback_value": 5
    }

    response = client.post(f"{API_GATEWAY_URL}/feedback/tasks", json=data)

    print("Response Status:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 200, f"Errore HTTP: {response.status_code} - {response.text}"
    json_response = response.json()
    assert json_response["status"] == "success"
    assert json_response["message"] == "Task feedback received"

def test_feedback_invalid_json(client):
    """ Testa l'errore quando il corpo della richiesta non è un JSON valido """

    response = client.post(f"{API_GATEWAY_URL}/feedback/domain", data="invalid data", headers={"Content-Type": "text/plain"})

    print("Response Status:", response.status_code)
    print("Response JSON:", response.text)

    assert response.status_code == 400, f"Errore HTTP: {response.status_code} - {response.text}"
    json_response = response.json()
    assert json_response["status"] == "failure"
    assert "Request body must be JSON" in json_response["motivation"]

