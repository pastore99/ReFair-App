import pytest
import gensim
import pickle
import numpy as np
from unittest.mock import MagicMock
from server.microservices.services.task_model_service import TaskModelService

@pytest.fixture
def mock_models(mocker):
    """ Mock per simulare il caricamento dei modelli """

    # Mock per GloVe
    mock_glove = MagicMock()
    mocker.patch("gensim.models.KeyedVectors.load_word2vec_format", return_value=mock_glove)

    # Mock per pickle (mlb e lsvc)
    mock_mlb = MagicMock()
    mock_lsvc = MagicMock()

    mocker.patch("pickle.load", side_effect=[mock_mlb, mock_lsvc])

@pytest.fixture
def task_model_service(mock_models):
    """ Crea un'istanza di TaskModelService con i modelli mockati """
    return TaskModelService()

def test_predict_task_success(task_model_service, mocker):
    """ Testa la predizione delle task con un input vettorizzato """

    mock_vectorized_text = np.array([[0.1, 0.2, 0.3]])  # Input finto

    # Mockiamo il comportamento del modello di predizione
    task_model_service.lsvc.predict.return_value = np.array([[1, 0]])
    task_model_service.mlb.inverse_transform.return_value = [("classification", "risk analysis")]

    tasks = task_model_service.predict_task(mock_vectorized_text)

    assert tasks == ["classification", "risk analysis"]

def test_glove_file_missing(mocker):
    """ Testa che venga sollevato un errore se il file GloVe è mancante """

    mocker.patch("os.path.exists", side_effect=lambda path: False if "glove.6B.100d.txt" in path else True)

    with pytest.raises(FileNotFoundError, match="GloVe model file not found"):
        TaskModelService()

def test_model_files_missing(mocker):
    """ Testa che venga sollevato un errore se i file del modello sono mancanti """

    mocker.patch("os.path.exists", side_effect=lambda path: False if "multilabel.pkl" in path or "LinearSVC_LabelPowerset.pkl" in path else True)

    with pytest.raises(FileNotFoundError, match="One or more model files are missing"):
        TaskModelService()

def test_predict_task_failure(task_model_service):
    """ Testa il caso in cui il modello di predizione fallisce """

    mock_vectorized_text = np.array([[0.1, 0.2, 0.3]])

    # Simuliamo un errore durante la predizione
    task_model_service.lsvc.predict.side_effect = ValueError("Prediction failed")

    with pytest.raises(ValueError, match="Prediction failed"):
        task_model_service.predict_task(mock_vectorized_text)
