import  sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../server/microservices')))

import pytest
import json
from domain_prediction_service import app

@pytest.fixture
def client():
    """ Crea un client di test per il server Flask """
    app.config['TESTING'] = True
    client = app.test_client()
    return client

def test_predict_domain_success(client, mocker):
    """ Testa la predizione con una user story valida """
    mocker.patch("server.microservices.domain_prediction_service.domain_classifier.predict", return_value="Cardiology")

    response = client.post('/predict/domain', data=json.dumps({
        "user_story": "As a cardiologist, I want to identify risk factors for heart disease."
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['domain'] == "Cardiology"

def test_predict_domain_no_json(client):
    """ Testa il caso in cui la richiesta non è JSON """
    response = client.post('/predict/domain', data="Not a JSON", content_type='text/plain')

    assert response.status_code == 400
    assert response.json['status'] == 'failure'
    assert response.json['motivation'] == "Request body must be JSON"

def test_predict_domain_missing_user_story(client):
    """ Testa il caso in cui manca il campo 'user_story' """
    response = client.post('/predict/domain', data=json.dumps({}), content_type='application/json')

    assert response.status_code == 400
    assert response.json['status'] == 'failure'
    assert response.json['motivation'] == "Missing 'user_story' in request"

def test_predict_domain_classifier_error(client, mocker):
    """ Testa la gestione degli errori interni del classificatore """
    mocker.patch("server.microservices.domain_prediction_service.domain_classifier.predict", side_effect=Exception("Model crashed"))

    response = client.post('/predict/domain', data=json.dumps({
        "user_stories": "As a software engineer, I want to automate testing."
    }), content_type='application/json')

    print("\nResponse JSON:", response.json)  # Debug: stampa la risposta JSON
    print("\nStatus Code:", response.status_code)  # Debug: stampa lo status code

    assert response.status_code == 400  # <-- Verifica se lo status è 400

