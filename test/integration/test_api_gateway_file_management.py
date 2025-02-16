import pytest
import requests
from io import BytesIO
import pandas as pd

API_GATEWAY_URL = "http://localhost:8080"

@pytest.fixture
def client():
    """ Restituisce un client di test per l'API Gateway """
    return requests.Session()

def test_stories_load_success(client):
    """Testa il caricamento di un file Excel valido attraverso API Gateway"""

    # Creiamo un file Excel in memoria
    excel_buffer = BytesIO()
    df = pd.DataFrame({"User Story": ["Story 1", "Story 2"]})  # Simuliamo dati validi
    df.to_excel(excel_buffer, index=False, engine="openpyxl")
    excel_buffer.seek(0)  # Riporta il puntatore all'inizio del file

    # File da inviare
    files = {
        "stories": ("test.xlsx", excel_buffer, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }

    # Effettua la richiesta
    response = client.post(f"{API_GATEWAY_URL}/storiesload", files=files)

    # Debug: Stampa la risposta per capire il problema
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

    # Estrarre la lista di user stories correttamente
    stories_dict = json_response.get("stories", {})
    stories_list = stories_dict.get("stories", [])

    assert isinstance(stories_list, list), f"Expected list, got {type(stories_list)}: {stories_list}"
    assert len(stories_list) > 0, "Nessuna user story ricevuta"

def test_stories_load_no_file(client):
    """ Testa l'errore quando non viene inviato alcun file """

    response = client.post(f"{API_GATEWAY_URL}/storiesload")

    print("Response Status:", response.status_code)
    print("Response JSON:", response.text)

    assert response.status_code == 400, f"Errore HTTP: {response.status_code} - {response.text}"
