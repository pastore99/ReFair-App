import pytest
import json
import os
from datetime import datetime
from server.microservices.services.feedback_manager import FeedbackManager

@pytest.fixture
def mock_feedback_file(tmpdir):
    """ Crea un file JSON temporaneo per i test """
    return os.path.join(tmpdir, "feedback_test.json")

@pytest.fixture
def mock_retrain_callback(mocker):
    """ Mock per simulare il callback di retraining """
    return mocker.Mock()

def test_save_feedback_success(mock_feedback_file, mock_retrain_callback):
    """ Testa il salvataggio di un feedback in un file JSON """

    feedback_manager = FeedbackManager(mock_feedback_file, feedback_threshold=10, retrain_callback=mock_retrain_callback)

    entry = {
        "user_story": "As a doctor, I want to analyze patient data to detect anomalies.",
        "predicted_domain": "Healthcare",
        "feedback_value": 5
    }

    feedback_manager.save_feedback(entry)

    with open(mock_feedback_file, "r") as f:
        feedback_list = json.load(f)

    assert len(feedback_list) == 1
    assert feedback_list[0]["user_story"] == "As a doctor, I want to analyze patient data to detect anomalies."
    assert "timestamp" in feedback_list[0]

def test_save_feedback_with_corrupted_json(mock_feedback_file, mock_retrain_callback):
    """ Testa il comportamento se il file JSON è corrotto """

    # Scriviamo manualmente un JSON corrotto nel file temporaneo
    with open(mock_feedback_file, "w") as f:
        f.write("invalid json")

    feedback_manager = FeedbackManager(mock_feedback_file, feedback_threshold=10, retrain_callback=mock_retrain_callback)

    entry = {
        "user_story": "As a scientist, I want to process data efficiently.",
        "predicted_domain": "Science",
        "feedback_value": 3
    }

    # Il metodo dovrebbe sovrascrivere il file corrotto con una nuova lista
    feedback_manager.save_feedback(entry)

    # Ora leggiamo il file che dovrebbe essere stato sovrascritto correttamente
    with open(mock_feedback_file, "r") as f:
        feedback_list = json.load(f)

    assert len(feedback_list) == 1  # Il file deve contenere solo il nuovo feedback
    assert feedback_list[0]["user_story"] == "As a scientist, I want to process data efficiently."

def test_retrain_called_when_threshold_reached(mock_feedback_file, mock_retrain_callback):
    """ Testa che il retraining venga attivato quando si raggiunge la soglia """

    # Scriviamo manualmente 9 feedback nel file per simulare il quasi raggiungimento della soglia
    initial_feedback = [{"user_story": "Existing entry"}] * 9
    with open(mock_feedback_file, "w") as f:
        json.dump(initial_feedback, f)

    feedback_manager = FeedbackManager(mock_feedback_file, feedback_threshold=10, retrain_callback=mock_retrain_callback)

    # Aggiungiamo il decimo feedback
    entry = {
        "user_story": "As a researcher, I want to test AI models.",
        "predicted_domain": "AI",
        "feedback_value": 4
    }

    feedback_manager.save_feedback(entry)

    # Verifichiamo che la funzione di retraining sia stata chiamata
    mock_retrain_callback.assert_called_once()

def test_create_file_if_not_exist(mock_feedback_file, mock_retrain_callback):
    """ Testa che il file venga creato se non esiste """

    feedback_manager = FeedbackManager(mock_feedback_file, feedback_threshold=10, retrain_callback=mock_retrain_callback)

    entry = {
        "user_story": "As a data analyst, I want to generate insights from data.",
        "predicted_domain": "Data Science",
        "feedback_value": 5
    }

    feedback_manager.save_feedback(entry)

    assert os.path.exists(mock_feedback_file)

    with open(mock_feedback_file, "r") as f:
        feedback_list = json.load(f)

    assert len(feedback_list) == 1
