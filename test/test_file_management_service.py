import  sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server/microservices')))

import io
import pytest
from file_management_service import app

@pytest.fixture
def client():
    """ Crea un client di test per il server Flask """
    app.config['TESTING'] = True
    client = app.test_client()
    return client

def test_load_stories_success(client, mocker):
    """ Testa il caricamento corretto di un file Excel """

    # Mock di un file Excel fittizio
    data = b"Fake Excel Data"
    file = (io.BytesIO(data), "stories.xlsx")

    # Mock del servizio ExcelParser per evitare elaborazioni reali
    mocker.patch("server.microservices.file_management_service.ExcelParser.parse_stories", return_value=[
        "As a developer, I want to test my API to ensure reliability."
    ])

    response = client.post('/storiesload', data={'stories': file}, content_type='multipart/form-data')

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert 'stories' in response.json
    assert len(response.json['stories']) > 0

def test_load_stories_no_file(client):
    """ Testa la risposta in caso di mancato upload del file """
    response = client.post('/storiesload', data={}, content_type='multipart/form-data')

    assert response.status_code == 200
    assert response.json['status'] == 'failure'
    assert "No file 'stories.xlsx' uploaded" in response.json['motivation']

def test_load_stories_invalid_file(client, mocker):
    """ Testa il comportamento con file Excel corrotto """

    # Mock di un file corrotto
    data = b"Corrupted Data"
    file = (io.BytesIO(data), "stories.xlsx")

    # Simuliamo un errore di parsing
    mocker.patch("server.microservices.file_management_service.ExcelParser.parse_stories", side_effect=ValueError("Invalid file format"))

    response = client.post('/storiesload', data={'stories': file}, content_type='multipart/form-data')

    assert response.status_code == 200
    assert response.json['status'] == 'failure'
    assert response.json['motivation'] == "Invalid file format"

