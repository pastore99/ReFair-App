import pytest
import json
import pandas as pd
from unittest.mock import patch, MagicMock
from server.microservices.services.classifier_factory import ClassifierFactory
from server.microservices.services.classifiers.xgboost_classifier import XGBoostDomainClassifier
from server.microservices.services.classifiers.bert_classifier import BERTDomainClassifier

@pytest.fixture
def mock_config_xgboost(mocker):
    """ Mock per simulare un config.json che usa XGBoost """
    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps({"default_algorithm": "xgboost"})))

@pytest.fixture
def mock_config_bert(mocker):
    """ Mock per simulare un config.json che usa BERT """
    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps({"default_algorithm": "bert"})))

@pytest.fixture
def mock_config_missing(mocker):
    """ Mock per simulare un config.json senza default_algorithm """
    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps({})))

@pytest.fixture
def mock_config_not_found(mocker):
    """ Mock per simulare l'assenza del file config.json """
    mocker.patch("builtins.open", side_effect=FileNotFoundError)

@pytest.fixture
def mock_xgboost_classifier(mocker):
    """ Mock per evitare di caricare il modello XGBoost, il dataset e il tokenizer BERT """

    # Mock del file di configurazione XGBoost
    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps({"default_algorithm": "xgboost"})))

    # Mock del dataset Excel (evita che cerchi di leggere un file reale)
    mocker.patch("pandas.read_excel", return_value=pd.DataFrame({"Feature": [1, 2, 3]}))

    # Mock di pickle.load per evitare che carichi un modello reale
    mocker.patch("pickle.load", return_value="Mocked Model")

    # 🛑 **Mock di `BertTokenizer.from_pretrained` per evitare di scaricare file**
    mock_tokenizer = MagicMock()
    mock_tokenizer.encode.return_value = [101, 102]  # Valori finti per encoding
    mocker.patch("server.microservices.services.classifiers.xgboost_classifier.BertTokenizer.from_pretrained", return_value=mock_tokenizer)

def test_get_xgboost_classifier(mock_config_xgboost, mock_xgboost_classifier):
    """ Testa che il factory restituisca XGBoost quando specificato in config.json """
    classifier = ClassifierFactory.get_domain_classifier()
    assert isinstance(classifier, XGBoostDomainClassifier)

def test_get_bert_classifier(mock_config_bert):
    """ Testa che il factory restituisca BERT quando specificato in config.json """
    classifier = ClassifierFactory.get_domain_classifier()
    assert isinstance(classifier, BERTDomainClassifier)

def test_get_default_xgboost_if_config_missing_key(mock_config_missing, mock_xgboost_classifier):
    """ Testa che il factory restituisca XGBoost se config.json non ha default_algorithm """
    classifier = ClassifierFactory.get_domain_classifier()
    assert isinstance(classifier, XGBoostDomainClassifier)

def test_get_default_xgboost_if_config_not_found(mock_config_not_found, mock_xgboost_classifier):
    """ Testa che il factory restituisca XGBoost se config.json non esiste """
    classifier = ClassifierFactory.get_domain_classifier()
    assert isinstance(classifier, XGBoostDomainClassifier)
