import pytest
import pandas as pd
import io
from server.microservices.services.excel_parser import ExcelParser

def test_parse_stories_success(mocker):
    """ Testa il parsing corretto di un file Excel valido """

    # Creiamo un DataFrame finto con la colonna 'User Story'
    mock_data = pd.DataFrame({"User Story": ["Story 1", "Story 2", "Story 3"]})

    # Mockiamo il comportamento di pd.read_excel per restituire il DataFrame finto
    mocker.patch("pandas.read_excel", return_value=mock_data)

    result = ExcelParser.parse_stories("fake_path.xlsx")

    assert result == ["Story 1", "Story 2", "Story 3"]

def test_parse_stories_missing_column(mocker):
    """ Testa il caso in cui manca la colonna 'User Story' """

    mock_data = pd.DataFrame({"Wrong Column": ["Story 1", "Story 2"]})

    mocker.patch("pandas.read_excel", return_value=mock_data)

    with pytest.raises(ValueError, match="No column 'User Story' found in the file"):
        ExcelParser.parse_stories("fake_path.xlsx")

def test_parse_stories_invalid_file(mocker):
    """ Testa il caso in cui il file non è un Excel valido """

    mocker.patch("pandas.read_excel", side_effect=ValueError("Invalid Excel file"))

    with pytest.raises(ValueError, match="Error reading Excel file: Invalid Excel file"):
        ExcelParser.parse_stories("fake_path.xlsx")

def test_parse_stories_file_not_found(mocker):
    """ Testa il caso in cui il file non esiste """

    mocker.patch("pandas.read_excel", side_effect=FileNotFoundError("File not found"))

    with pytest.raises(ValueError, match="Error reading Excel file: File not found"):
        ExcelParser.parse_stories("non_existent.xlsx")
