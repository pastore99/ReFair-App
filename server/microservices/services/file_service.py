import os

ALLOWED_EXTENSIONS = {'xlsx'}

class FileService:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        os.makedirs(self.upload_folder, exist_ok=True)  # Crea la cartella se non esiste

    def allowed_file(self, filename):
        """
        Check extension of input file

        :param filename: the name of input file
        :return: true if extension is in ALLOWED_EXTENSIONS, else false
        """
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def save_file(self, file, filename):
        """
        Save file in locale directory.

        :param file: FileStorage  object
        :param filename: the name of input file
        :return: the path save
        """
        if not self.allowed_file(filename):
            raise ValueError("This type of file is not supported. Upload an xlsx file.")

        file_path = os.path.join(self.upload_folder, filename)
        file.save(file_path)
        return file_path