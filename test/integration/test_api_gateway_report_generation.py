import pytest
import requests

API_GATEWAY_URL = "http://localhost:8080"

@pytest.fixture
def client():
    """ Restituisce un client di test per l'API Gateway """
    return requests.Session()

def test_generate_report_success(client):
    """ Testa la generazione del report con user stories valide """

    data = {
        "user_stories": [
            "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease."
        ]
    }

    response = client.post(f"{API_GATEWAY_URL}/generate/report", json=data)

    # Debugging: Mostra la risposta completa in caso di errore
    print("\n--- DEBUG RESPONSE ---")
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Response Body:", response.text)

    assert response.status_code == 200, f"Errore HTTP: {response.status_code} - {response.text}"

    try:
        json_response = response.json()
    except ValueError:
        assert False, f"Risposta non in formato JSON: {response.text}"

    # Controlli sugli output attesi
    assert isinstance(json_response, list), "La risposta deve essere una lista di report"
    assert len(json_response) > 0, "Il report non contiene user stories"
    assert "user_story" in json_response[0], "Campo 'user_story' mancante nel report"

def test_generate_report_invalid_json(client):
    """ Testa l'errore quando il corpo della richiesta non è un JSON valido """

    response = client.post(f"{API_GATEWAY_URL}/generate/report", data="invalid data", headers={"Content-Type": "text/plain"})

    assert response.status_code == 400, f"Errore HTTP: {response.status_code} - {response.text}"

    try:
        json_response = response.json()
    except ValueError:
        assert False, f"Risposta non in formato JSON: {response.text}"

    assert json_response["status"] == "failure"
    assert "Request body must be JSON" in json_response["motivation"]

def test_generate_report_missing_user_stories(client):
    """ Testa l'errore quando manca il campo 'user_stories' """

    response = client.post(f"{API_GATEWAY_URL}/generate/report", json={})

    # Debugging: Mostra la risposta in caso di errore
    print("\n--- DEBUG RESPONSE ---")
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 400, f"Errore HTTP: {response.status_code} - {response.text}"

    try:
        json_response = response.json()
    except ValueError:
        assert False, f"Risposta non in formato JSON: {response.text}"

    assert json_response["status"] == "failure"
    assert "Missing 'user_stories'" in json_response["motivation"]
