import  sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../server/microservices')))

import pytest
import json
from flask import Flask
from feedback_service import app  # Assumendo che il file principale si chiami feedback_service.py

@pytest.fixture
def client():
    """ Crea un client di test per il server Flask """
    app.config['TESTING'] = True
    client = app.test_client()
    return client

# Test per l'endpoint /feedback/domain
def test_feedback_domain_success(client, mocker):
    """ Testa l'invio di feedback valido per il dominio """
    mocker.patch("services.feedback_manager.FeedbackManager.save_feedback", return_value=None)

    response = client.post('/feedback/domain', data=json.dumps({
        "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
        "predicted_domain": "Cardiology",
        "feedback_value": 4
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == "Domain feedback received"

# Test per l'endpoint /feedback/tasks
def test_feedback_tasks_success(client, mocker):
    """ Testa l'invio di feedback valido per le task """
    mocker.patch("services.feedback_manager.FeedbackManager.save_feedback", return_value=None)

    response = client.post('/feedback/tasks', data=json.dumps({
        "user_story": "As a transportation planner, I want to use inverse reinforcement learning to understand the underlying motivations and decision-making processes of drivers, so that I can improve traffic management and reduce accidents.",
        "domain": "Transportation",
        "predicted_tasks": ["pricing"],
        "feedback_value": 5
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == "Task feedback received"

# Test per richiesta non JSON
def test_feedback_no_json(client):
    """ Testa il caso in cui la richiesta non è in JSON """
    response = client.post('/feedback/domain', data="Invalid Text", content_type='text/plain')

    assert response.status_code == 415  # 415 Unsupported Media Type

# Test per campi mancanti
def test_feedback_missing_fields(client):
    """ Testa il caso in cui mancano i campi obbligatori nel feedback """
    response = client.post('/feedback/domain', data=json.dumps({"user_story": "As a surgeon..."}), content_type='application/json')

    assert response.status_code == 200  # 400 Bad Request
