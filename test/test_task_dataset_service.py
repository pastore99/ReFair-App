import pytest
import pandas as pd
import os
from unittest.mock import MagicMock
from server.microservices.services.task_dataset_service import TaskDatasetService

@pytest.fixture
def mock_datasets(mocker):
    """ Mock per simulare dataset caricati correttamente """
    mock_domain_task_mapping = pd.DataFrame({
        "Domain": ["Healthcare", "Healthcare", "Finance"],
        "Task": ["classification", "risk analysis", "fraud detection"]
    })

    mock_domains_mapping = pd.DataFrame({
        "Domain": ["Healthcare", "Finance"],
        "Feature": ["age", "salary"]
    })

    mock_tasks_mapping = pd.DataFrame({
        "Task": ["classification", "risk analysis", "fraud detection"],
        "Feature": ["age", "history", "transactions"]
    })

    # Mockiamo il comportamento di pd.read_csv
    mocker.patch("pandas.read_csv", side_effect=[mock_domain_task_mapping, mock_domains_mapping, mock_tasks_mapping])

@pytest.fixture
def task_dataset_service(mock_datasets):
    """ Crea un'istanza di TaskDatasetService con i dataset mockati """
    return TaskDatasetService()

def test_get_tasks_for_domain_success(task_dataset_service):
    """ Testa il recupero delle task per un dominio valido """

    result = task_dataset_service.get_tasks_for_domain("Healthcare", ["classification", "risk analysis", "fraud detection"])

    assert result == ["classification", "risk analysis"]  # fraud detection non è presente in Healthcare

def test_get_tasks_for_domain_invalid_domain(task_dataset_service):
    """ Testa che venga sollevato un errore se il dominio non è una stringa """

    with pytest.raises(TypeError, match="Expected domain as str"):
        task_dataset_service.get_tasks_for_domain(123, ["classification"])

def test_get_tasks_for_domain_invalid_task(task_dataset_service):
    """ Testa che venga sollevato un errore se una task non è una stringa """

    with pytest.raises(TypeError, match="Expected task as str"):
        task_dataset_service.get_tasks_for_domain("Healthcare", ["classification", 123])

def test_extract_features_success(task_dataset_service):
    """ Testa l'estrazione delle feature per un dominio e task validi """

    result = task_dataset_service.extract_features("Healthcare", ["classification", "risk analysis"])

    assert result == {
        "classification": ["age"],  # Intersezione tra domain e task feature
        "risk analysis": []
    }

def test_extract_features_invalid_domain(task_dataset_service):
    """ Testa che venga sollevato un errore se il dominio non è una stringa """

    with pytest.raises(TypeError, match="Expected domain as str"):
        task_dataset_service.extract_features(123, ["classification"])

def test_extract_features_invalid_task(task_dataset_service):
    """ Testa che venga sollevato un errore se una task non è una stringa """

    with pytest.raises(TypeError, match="Expected task as str"):
        task_dataset_service.extract_features("Healthcare", ["classification", 123])

def test_missing_datasets(mocker):
    """ Testa che venga sollevato un errore se i file dataset sono mancanti """

    mocker.patch("os.path.exists", return_value=False)

    with pytest.raises(FileNotFoundError, match="One or more dataset files are missing"):
        TaskDatasetService()
