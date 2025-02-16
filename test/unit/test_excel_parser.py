import pytest
import pandas as pd
import re
from unittest.mock import MagicMock
from server.microservices.services.excel_parser import ExcelParser

PATTERN = r'^(?!\s*$).{1,1024}$'

def test_parse_stories_success(mocker):
    """ Testa il parsing corretto di un file Excel valido """

    mock_data = pd.DataFrame({"User Story": ["Story 1", "Story 2", "Story 3"]})

    mocker.patch("pandas.read_excel", return_value=mock_data)

    result = ExcelParser.parse_stories("fake_path.xlsx")

    assert result["stories"] == ["Story 1", "Story 2", "Story 3"]
    assert result["warning"] is None  # Nessun warning atteso

def test_parse_stories_missing_column(mocker):
    """ Testa il caso in cui manca la colonna 'User Story' """

    mock_data = pd.DataFrame({"Wrong Column": ["Story 1", "Story 2"]})

    mocker.patch("pandas.read_excel", return_value=mock_data)

    result = ExcelParser.parse_stories("fake_path.xlsx")

    assert "error" in result
    assert result["error"] == "No column 'User Story' found in the file"

def test_parse_stories_non_textual_values(mocker):
    """ Testa il caso in cui la colonna contiene valori non testuali """

    mock_data = pd.DataFrame({"User Story": ["Valid Story", 123, None, "Another Story"]})

    mocker.patch("pandas.read_excel", return_value=mock_data)

    result = ExcelParser.parse_stories("fake_path.xlsx")

    assert "error" in result
    assert result["error"] == "The file could not be loaded because at least one non-textual element was found in the 'User Story' column."

def test_parse_stories_empty_file(mocker):
    """ Testa il caso in cui il file è vuoto """

    mock_data = pd.DataFrame({"User Story": []})

    mocker.patch("pandas.read_excel", return_value=mock_data)

    result = ExcelParser.parse_stories("fake_path.xlsx")

    assert "error" in result
    assert result["error"] == "There are no user stories"

def test_parse_stories_invalid_format(mocker):
    """ Testa il caso in cui alcune storie non rispettano il formato """

    mock_data = pd.DataFrame({"User Story": ["Valid Story", "   ", "Another Valid Story", "", "Too long " * 500]})

    mocker.patch("pandas.read_excel", return_value=mock_data)

    result = ExcelParser.parse_stories("fake_path.xlsx")

    assert result["stories"] == ["Valid Story", "Another Valid Story"]  # Solo le valide vengono mantenute
    assert result["warning"] == "The file was loaded successfully, but some user stories did not match the required format and were not included."

def test_parse_stories_invalid_file(mocker):
    """ Testa il caso in cui il file non è un Excel valido """

    mocker.patch("pandas.read_excel", side_effect=ValueError("Invalid Excel file"))

    result = ExcelParser.parse_stories("fake_path.xlsx")

    assert "error" in result
    assert result["error"] == "Invalid Excel file"

def test_parse_stories_file_not_found(mocker):
    """ Testa il caso in cui il file non esiste """

    mocker.patch("pandas.read_excel", side_effect=FileNotFoundError("File not found"))

    result = ExcelParser.parse_stories("non_existent.xlsx")

    assert "error" in result
    assert result["error"] == "File not found"
