import pytest
import requests

API_GATEWAY_URL = "http://localhost:8080"

@pytest.fixture
def client():
    """ Restituisce un client di test per l'API Gateway """
    return requests.Session()

def test_predict_tasks_success(client):
    """ Testa la predizione dei task con una user story valida """

    data = {
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
        "domain": "Cardiology"
    }

    response = client.post(f"{API_GATEWAY_URL}/predict/tasks", json=data)

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
    assert json_response["status"] == "success", "Lo stato della risposta non è 'success'"
    assert isinstance(json_response["tasks"], list), "Il campo 'tasks' deve essere una lista"
    assert len(json_response["tasks"]) > 0, "Nessun task restituito nella risposta"

def test_predict_tasks_invalid_json(client):
    """ Testa l'errore quando il corpo della richiesta non è un JSON valido """

    response = client.post(f"{API_GATEWAY_URL}/predict/tasks", data="invalid data", headers={"Content-Type": "text/plain"})

    assert response.status_code == 400, f"Errore HTTP: {response.status_code} - {response.text}"

    try:
        json_response = response.json()
    except ValueError:
        assert False, f"Risposta non in formato JSON: {response.text}"

    assert json_response["status"] == "failure"
    assert "Request body must be JSON" in json_response["motivation"]

