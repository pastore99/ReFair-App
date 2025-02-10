import  sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server/microservices')))

import pytest
import json
from feedback_service import app

@pytest.fixture
def client():
    """ Crea un client di test per il server Flask """
    app.config['TESTING'] = True
    client = app.test_client()
    return client

def test_feedback_domain_success(client, mocker):
    """ Testa l'invio di feedback valido per il dominio """

    mocker.patch("server.microservices.feedback_service.domain_feedback_manager.save_feedback", return_value=None)

    response = client.post('/feedback/domain', data=json.dumps({
        "user_story": "A group of researchers is using abstractive summarization to identify key trends and insights in large sets of biological data, enabling more efficient analysis and interpretation.",
        "predicted_domain": "Biology",
        "feedback_value": 4
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == "Domain feedback received"

def test_feedback_tasks_success(client, mocker):
    """ Testa l'invio di feedback valido per le task """

    mocker.patch("server.microservices.feedback_service.task_feedback_manager.save_feedback", return_value=None)

    response = client.post('/feedback/tasks', data=json.dumps({
        "user_story": "A group of researchers is using abstractive summarization to identify key trends and insights in large sets of biological data, enabling more efficient analysis and interpretation.",
        "domain": "Biology",
        "predicted_tasks": ["abstractive summarization"],
        "feedback_value": 5
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == "Task feedback received"

def test_feedback_no_json(client):
    """ Testa il caso in cui la richiesta non è in JSON """
    response = client.post('/feedback/domain', data="Invalid Text", content_type='text/plain')

    assert response.status_code == 415

def test_feedback_missing_fields(client):
    """ Testa il caso in cui mancano i campi obbligatori nel feedback """

    response = client.post('/feedback/domain', data=json.dumps({"user_story": "As a surgeon..."}), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == 'success'
