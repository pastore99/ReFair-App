import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock
from server.microservices.services.task_preprocessor import TaskPreprocessor

@pytest.fixture
def mock_glove_vectors():
    """ Mock per il modello GloVe """
    mock_glove = {
        "doctor": np.array([0.1] * 100),
        "patient": np.array([0.2] * 100),
        "data": np.array([0.3] * 100)
    }
    return mock_glove

@pytest.fixture
def task_preprocessor(mock_glove_vectors):
    """ Crea un'istanza di TaskPreprocessor con il modello GloVe mockato """
    return TaskPreprocessor(mock_glove_vectors)

def test_preprocess_success(task_preprocessor):
    """ Testa la conversione di un testo con parole presenti in GloVe """

    result = task_preprocessor.preprocess("doctor patient data")

    assert result.shape == (1, 100)  # Deve essere un array 2D con 1 riga e 100 colonne
    assert np.all(result >= 0)  # I valori devono essere >= 0 (media di embedding positivi)

def test_preprocess_unknown_words(task_preprocessor):
    """ Testa il comportamento con parole non presenti in GloVe """

    result = task_preprocessor.preprocess("unknownword1 unknownword2")

    assert result.shape == (1, 100)  # Deve essere un array 2D con 1 riga e 100 colonne
    assert np.all(result == 0)  # Deve essere un vettore nullo se nessuna parola è in GloVe

def test_preprocess_empty_string(task_preprocessor):
    """ Testa il comportamento con un testo vuoto """

    result = task_preprocessor.preprocess("")

    assert result.shape == (1, 100)  # Deve essere un array 2D con 1 riga e 100 colonne
    assert np.all(result == 0)  # Deve essere un vettore nullo

def test_preprocess_invalid_input(task_preprocessor):
    """ Testa che venga sollevato un errore se l'input non è una stringa """

    with pytest.raises(AttributeError):
        task_preprocessor.preprocess(123)  # Un numero non ha il metodo split()
