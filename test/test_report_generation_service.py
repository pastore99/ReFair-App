import  sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server/microservices')))

import pytest
import json
from report_generation_service import app

@pytest.fixture
def client():
    """ Crea un client di test per il server Flask """
    app.config['TESTING'] = True
    client = app.test_client()
    return client

def test_generate_report_success(client, mocker):
    """ Testa la generazione del report con user stories valide """

    mock_report = json.dumps([
        {
            "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
            "domain": "Cardiology",
            "tasks": ["classification", "ranking"],
            "tasks_features": {
                "classification": ["race", "age", "sex"],
                "ranking": ["race", "age", "sex"]
            }
        }
    ])

    mocker.patch("server.microservices.report_generation_service.report_generator.generate", return_value=mock_report)

    response = client.post('/generate/report', data=json.dumps({
        "user_stories": ["As a cardiologist, I want to identify multiword expressions in patient notes."]
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.mimetype == 'application/json'
    assert 'attachment;filename=report.json' in response.headers['Content-Disposition']

def test_generate_report_no_json(client):
    """ Testa il caso in cui la richiesta non è JSON """
    response = client.post('/generate/report', data="Invalid Text", content_type='text/plain')

    assert response.status_code == 200
    assert response.json['status'] == 'failure'
    assert response.json['motivation'] == "Request body must be JSON"

def test_generate_report_missing_user_stories(client):
    """ Testa il caso in cui manca il campo 'user_stories' o non è una lista """
    response = client.post('/generate/report', data=json.dumps({}), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == 'failure'
    assert response.json['motivation'] == "Missing 'user_stories' (list) in request"

    response = client.post('/generate/report', data=json.dumps({"user_stories": "Not a list"}), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == 'failure'
    assert response.json['motivation'] == "Missing 'user_stories' (list) in request"

def test_generate_report_error(client, mocker):
    """ Testa il caso in cui la generazione del report fallisce, restituendo domini e task vuoti """

    # Simuliamo che il report generator restituisca un report vuoto
    mocker.patch("server.microservices.report_generation_service.report_generator.generate", return_value=json.dumps([]))

    response = client.post('/generate/report', data=json.dumps({
        "user_stories": ["As a cardiologist, I want to identify multiword expressions in patient notes."]
    }), content_type='application/json')

    # Stampa il risultato per debug
    print("\nResponse JSON:", response.json)
    print("\nStatus Code:", response.status_code)

    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 1

