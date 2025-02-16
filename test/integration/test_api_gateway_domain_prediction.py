import pytest
import requests

API_GATEWAY_URL = "http://localhost:8080"

@pytest.fixture
def client():
    """ Restituisce un client di test per l'API Gateway """
    return requests.Session()

def test_predict_domain_success(client):
    """ Testa la predizione del dominio con una user story valida """

    data = {
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease."
    }

    response = client.post(f"{API_GATEWAY_URL}/predict/domain", json=data)

    print("Response Status:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 200, f"Errore HTTP: {response.status_code} - {response.text}"
    json_response = response.json()
    assert json_response["status"] == "success"
    assert isinstance(json_response["domain"], str) and len(json_response["domain"]) > 0

def test_predict_domain_invalid_json(client):
    """ Testa l'errore quando il corpo della richiesta non è un JSON valido """

    response = client.post(f"{API_GATEWAY_URL}/predict/domain", data="invalid data", headers={"Content-Type": "text/plain"})

    print("Response Status:", response.status_code)
    print("Response JSON:", response.text)

    assert response.status_code == 400, f"Errore HTTP: {response.status_code} - {response.text}"
    json_response = response.json()
    assert json_response["status"] == "failure"
    assert "Request body must be JSON" in json_response["motivation"]

def test_predict_domain_missing_user_story(client):
    """ Testa l'errore quando manca il campo 'user_story' """

    data = {"user_story": ""}  # Simula un input vuoto

    response = client.post(f"{API_GATEWAY_URL}/predict/domain", json=data)

    print("Response Status:", response.status_code)
    print("Response JSON:", response.text)

    assert response.status_code == 400, f"Errore HTTP: {response.status_code} - {response.text}"
    json_response = response.json()
    assert json_response["status"] == "failure"
    assert "Missing 'user_story'" in json_response["motivation"]

