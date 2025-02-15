import  sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server/microservices')))

import pytest
import json
from task_prediction_service import app

@pytest.fixture
def client():
    """ Crea un client di test per il server Flask """
    app.config['TESTING'] = True
    client = app.test_client()
    return client

def test_predict_tasks_success(client, mocker):
    """ Testa la predizione con una user story e dominio validi """

    mocker.patch("server.microservices.task_prediction_service.preprocessor.preprocess", return_value=[0.5, 0.3, 0.2])
    mocker.patch("server.microservices.task_prediction_service.model_service.predict_task", return_value=["classification", "ranking"])
    mocker.patch("server.microservices.task_prediction_service.dataset_service.get_tasks_for_domain", return_value=["classification", "ranking"])
    mocker.patch("server.microservices.task_prediction_service.dataset_service.extract_features", return_value={
        "classification": ["race", "age", "sex"],
        "ranking": ["race", "age", "sex"]
    })

    response = client.post('/predict/tasks', data=json.dumps({
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
        "domain": "Cardiology"
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['tasks'] == ["classification", "ranking"]
    assert "classification" in response.json['tasks_features']

def test_predict_tasks_no_json(client):
    """ Testa il caso in cui la richiesta non è JSON """
    response = client.post('/predict/tasks', data="Invalid Text", content_type='text/plain')

    assert response.status_code == 400
    assert response.json['status'] == 'failure'
    assert response.json['motivation'] == "Request body must be JSON"

def test_predict_tasks_missing_fields(client):
    """ Testa il caso in cui manca 'user_story' o 'domain' """
    response = client.post('/predict/tasks', data=json.dumps({"user_story": "As a cardiologist..."}), content_type='application/json')

    assert response.status_code == 400
    assert response.json['status'] == 'failure'
    assert response.json['motivation'] == "Missing 'user_story' or 'domain' in request"

def test_predict_tasks_preprocessor_error(client, mocker):
    """ Testa il caso in cui il pre-processing genera un errore """
    mocker.patch("server.microservices.task_prediction_service.preprocessor.preprocess", return_value=None)  # Il preprocessing fallisce

    response = client.post('/predict/tasks', data=json.dumps({
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes.",
        "domain": "Cardiology"
    }), content_type='application/json')

    assert response.status_code == 200  # Ora ci aspettiamo 200 invece di 500
    assert response.json['status'] == 'success'  # Il sistema deve gestire il fallimento restituendo success con tasks vuote
    assert response.json['tasks'] == []  # Nessuna task trovata
    assert response.json['tasks_features'] == {}  # Nessuna feature trovata

def test_predict_tasks_no_tasks_found(client, mocker):
    """ Testa il caso in cui la predizione non trova task (array vuoto) """
    mocker.patch("server.microservices.task_prediction_service.preprocessor.preprocess", return_value=[0.5, 0.3, 0.2])
    mocker.patch("server.microservices.task_prediction_service.model_service.predict_task", return_value=[])
    mocker.patch("server.microservices.task_prediction_service.dataset_service.get_tasks_for_domain", return_value=[])
    mocker.patch("server.microservices.task_prediction_service.dataset_service.extract_features", return_value={})

    response = client.post('/predict/tasks', data=json.dumps({
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes.",
        "domain": "Cardiology"
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['tasks'] == []
    assert response.json['tasks_features'] == {}

def test_predict_tasks_dataset_no_tasks(client, mocker):
    """ Testa il caso in cui il dataset service non trova task per il dominio """
    mocker.patch("server.microservices.task_prediction_service.preprocessor.preprocess", return_value=[0.5, 0.3, 0.2])
    mocker.patch("server.microservices.task_prediction_service.model_service.predict_task", return_value=["classification", "ranking"])
    mocker.patch("server.microservices.task_prediction_service.dataset_service.get_tasks_for_domain", return_value=[])
    mocker.patch("server.microservices.task_prediction_service.dataset_service.extract_features", return_value={})

    response = client.post('/predict/tasks', data=json.dumps({
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes.",
        "domain": "Cardiology"
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['tasks'] == []
    assert response.json['tasks_features'] == {}

