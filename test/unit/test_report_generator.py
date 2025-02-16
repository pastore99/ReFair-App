import pytest
import json
from unittest.mock import MagicMock
from server.microservices.services.report_generator import ReportGenerator

@pytest.fixture
def mock_prediction_service():
    """ Mock per PredictionService """
    return MagicMock()

@pytest.fixture
def report_generator(mock_prediction_service):
    """ Crea un'istanza di ReportGenerator con il PredictionService mockato """
    return ReportGenerator(mock_prediction_service)

def test_generate_report_success(report_generator, mock_prediction_service):
    """ Testa la generazione di un report con successo """

    mock_prediction_service.get_domain.return_value = "Healthcare"
    mock_prediction_service.get_tasks.return_value = (
        ["classification", "risk analysis"],
        {"classification": ["age", "race"], "risk analysis": ["sex", "history"]}
    )

    user_stories = ["As a doctor, I want to analyze patient data."]
    report = report_generator.generate(user_stories)
    report_data = json.loads(report)

    assert len(report_data) == 1
    assert report_data[0]["domain"] == "Healthcare"
    assert report_data[0]["tasks"] == ["classification", "risk analysis"]

def test_generate_report_domain_failure(report_generator, mock_prediction_service):
    """ Testa il caso in cui la predizione del dominio fallisce """

    mock_prediction_service.get_domain.side_effect = ValueError("Domain prediction failed")

    user_stories = ["As a doctor, I want to analyze patient data."]
    report = report_generator.generate(user_stories)
    report_data = json.loads(report)

    assert len(report_data) == 1
    assert report_data[0]["status"] == "failure"
    assert "Domain prediction failed" in report_data[0]["motivation"]

def test_generate_report_tasks_failure(report_generator, mock_prediction_service):
    """ Testa il caso in cui la predizione delle task fallisce """

    mock_prediction_service.get_domain.return_value = "Healthcare"
    mock_prediction_service.get_tasks.side_effect = ValueError("Task prediction failed")

    user_stories = ["As a doctor, I want to analyze patient data."]
    report = report_generator.generate(user_stories)
    report_data = json.loads(report)

    assert len(report_data) == 1
    assert report_data[0]["status"] == "failure"
    assert "Task prediction failed" in report_data[0]["motivation"]

def test_generate_report_mixed_results(report_generator, mock_prediction_service):
    """ Testa un report con più user stories, alcune con errori """

    mock_prediction_service.get_domain.side_effect = ["Healthcare", ValueError("Domain prediction failed")]
    mock_prediction_service.get_tasks.side_effect = [
        (["classification"], {"classification": ["age"]}),
        ValueError("Task prediction failed")
    ]

    user_stories = [
        "As a doctor, I want to analyze patient data.",
        "As a researcher, I want to study AI models."
    ]
    report = report_generator.generate(user_stories)
    report_data = json.loads(report)

    assert len(report_data) == 2

    # Prima storia deve avere predizione corretta
    assert report_data[0]["domain"] == "Healthcare"
    assert report_data[0]["tasks"] == ["classification"]

    # Seconda storia deve avere un errore
    assert report_data[1]["status"] == "failure"
    assert "Domain prediction failed" in report_data[1]["motivation"]
