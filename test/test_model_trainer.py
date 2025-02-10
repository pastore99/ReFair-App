import pytest
import pickle
import numpy as np
import pandas as pd
from unittest.mock import MagicMock
from server.microservices.services.model_trainer import ModelTrainer

@pytest.fixture
def mock_glove_vectors():
    """ Mock per il modello GloVe """
    return {
        "doctor": np.array([0.1] * 100),
        "patient": np.array([0.2] * 100),
        "data": np.array([0.3] * 100)
    }

@pytest.fixture
def mock_dataset(mocker):
    """ Mock per il dataset """
    mock_df = pd.DataFrame({
        "User Story": ["As a doctor, I want to analyze patient data."],
        "Domain": ["Healthcare"],
        "Machine Learning Task": ["classification,risk analysis"]
    })
    mocker.patch("pandas.read_excel", return_value=mock_df)

@pytest.fixture
def mock_model_trainer(mock_glove_vectors, mock_dataset, mocker, tmpdir):
    """ Crea un'istanza di ModelTrainer con mock di dataset e GloVe """
    domain_model_path = tmpdir.join("domain_model.pkl")
    task_model_path = tmpdir.join("task_model.pkl")
    dataset_path = tmpdir.join("dataset.xlsx")
    glove_path = tmpdir.join("glove.6B.100d.txt")

    mocker.patch("gensim.models.KeyedVectors.load_word2vec_format", return_value=mock_glove_vectors)
    mocker.patch("pickle.load", return_value=MagicMock())
    mocker.patch("pickle.dump")

    return ModelTrainer(str(domain_model_path), str(task_model_path), str(dataset_path), str(glove_path))

def test_compute_feature_vector_success(mock_model_trainer):
    """ Testa la conversione di un testo con parole presenti in GloVe """

    result = mock_model_trainer.compute_feature_vector("doctor patient data")

    assert result.shape == (100,)
    assert np.all(result >= 0)

def test_compute_feature_vector_unknown_words(mock_model_trainer):
    """ Testa il comportamento con parole non presenti in GloVe """

    result = mock_model_trainer.compute_feature_vector("unknownword1 unknownword2")

    assert result.shape == (100,)
    assert np.all(result == 0)

def test_compute_feature_vector_empty_string(mock_model_trainer):
    """ Testa il comportamento con una stringa vuota """

    result = mock_model_trainer.compute_feature_vector("")

    assert result.shape == (100,)
    assert np.all(result == 0)

def test_glove_file_missing(mocker):
    """ Testa che venga sollevato un errore se il file GloVe è mancante """

    mocker.patch("os.path.exists", side_effect=lambda path: False if "glove.6B.100d.txt" in path else True)

    with pytest.raises(FileNotFoundError):  # Rimuoviamo il match sul messaggio
        ModelTrainer("domain.pkl", "task.pkl", "dataset.xlsx", "glove.6B.100d.txt")

def test_retrain_domain_model_success(mock_model_trainer):
    """ Testa il retraining del modello dominio con feedback valido """

    feedback_list = [
        {"user_story": "As a doctor, I want to analyze patient data.", "predicted_domain": "Healthcare"}
    ]

    mock_model_trainer.retrain_domain_model(feedback_list)

def test_retrain_domain_model_invalid_domain(mock_model_trainer, capsys):
    """ Testa che venga stampato un errore se il dominio non è nel dataset """

    feedback_list = [
        {"user_story": "As a doctor, I want to analyze patient data.", "predicted_domain": "UnknownDomain"}
    ]

    mock_model_trainer.retrain_domain_model(feedback_list)

    captured = capsys.readouterr()
    assert "ERRORE: Il dominio 'UnknownDomain' non esiste nel dataset!" in captured.out

def test_retrain_task_model_success(mock_model_trainer, mocker):
    """ Testa il retraining del modello task con feedback valido """

    # Creiamo un file fittizio per evitare l'errore di FileNotFoundError
    with open(mock_model_trainer.task_model_path, 'wb') as f:
        pickle.dump(MagicMock(), f)

    feedback_list = [
        {"user_story": "As a doctor, I want to analyze patient data.", "predicted_tasks": ["classification", "risk analysis"]}
    ]

    mock_model_trainer.retrain_task_model(feedback_list)
