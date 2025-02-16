import pytest
import requests
from io import BytesIO

API_GATEWAY_URL = "http://localhost:8080"

@pytest.fixture
def client():
    """ Restituisce un client di test per l'API Gateway """
    return requests.Session()

def test_stories_load_success(client):
    """ Testa il caricamento di un file valido attraverso API Gateway """

    # File da inviare
    files = {
        "stories": ("test.xlsx", BytesIO(b"fake_excel_data"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }

    # Effettua la richiesta
    response = client.post(f"{API_GATEWAY_URL}/storiesload", files=files)

    # Debug: Stampa il contenuto della risposta per capire il problema
    print("\n--- DEBUG RESPONSE ---")
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Response Body:", response.text)

    # Verifica se lo status code è 200
    assert response.status_code == 200, f"Errore HTTP: {response.status_code} - {response.text}"

    try:
        json_response = response.json()
    except ValueError:
        assert False, f"Risposta non in formato JSON: {response.text}"

    # Controlli sugli output attesi
    assert json_response["status"] == "success", f"Errore: {json_response}"
    assert isinstance(json_response["stories"], list), "Il campo 'stories' non è una lista"
    assert len(json_response["stories"]) > 0, "Nessuna user story ricevuta"

def test_stories_load_no_file(client):
    """ Testa l'errore quando non viene inviato alcun file """

    response = client.post(f"{API_GATEWAY_URL}/storiesload")

    print("Response Status:", response.status_code)
    print("Response JSON:", response.text)

    assert response.status_code == 400, f"Errore HTTP: {response.status_code} - {response.text}"
