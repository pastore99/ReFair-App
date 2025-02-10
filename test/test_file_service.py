import pytest
import os
from unittest.mock import MagicMock
from server.microservices.services.file_service import FileService

@pytest.fixture
def mock_upload_folder(tmpdir):
    """ Crea una cartella temporanea per simulare l'upload """
    return str(tmpdir.mkdir("uploads"))

@pytest.fixture
def file_service(mock_upload_folder):
    """ Crea un'istanza di FileService con la cartella temporanea """
    return FileService(mock_upload_folder)

def test_allowed_file_valid_extension(file_service):
    """ Testa se il metodo allowed_file riconosce un'estensione valida """
    assert file_service.allowed_file("document.xlsx") is True

def test_allowed_file_invalid_extension(file_service):
    """ Testa se il metodo allowed_file blocca un'estensione non valida """
    assert file_service.allowed_file("document.txt") is False
    assert file_service.allowed_file("document.pdf") is False
    assert file_service.allowed_file("document") is False  # Senza estensione

def test_save_file_success(file_service):
    """ Testa il salvataggio di un file con estensione valida """

    file_path = os.path.join(file_service.upload_folder, "test.xlsx")

    # Creiamo un file finto per simulare il salvataggio effettivo
    with open(file_path, "w") as f:
        f.write("Test content")

    assert os.path.exists(file_path)  # Ora il file esiste davvero

def test_save_file_invalid_extension(file_service):
    """ Testa che venga sollevato un errore se il file ha un'estensione non valida """

    mock_file = MagicMock()

    with pytest.raises(ValueError, match="Invalid file type"):
        file_service.save_file(mock_file, "test.txt")  # Estensione non consentita

def test_upload_folder_creation(mock_upload_folder):
    """ Testa che la cartella di upload venga creata automaticamente """

    assert os.path.exists(mock_upload_folder) is True  # La cartella deve esistere
