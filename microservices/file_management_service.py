from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

# Configurazione Flask
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    """Controlla se il file caricato ha un'estensione consentita."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/storiesload', methods=['POST'])
def load_stories():
    if 'stories' not in request.files:
        return jsonify({
            'status': 'failure',
            'motivation': "No file 'stories.xlsx' loaded"
        })

    file = request.files['stories']

    if not allowed_file(file.filename):
        return jsonify({
            'status': 'failure',
            'motivation': "Invalid file type"
        })

    # Processa il file...


    stories = pd.read_excel(file)

    if 'User Story' in stories:
        return jsonify({
            'status': 'success',
            'stories': stories["User Story"].tolist()
        })
    else:
        return jsonify({
            'status': 'failure',
            'motivation': "No column 'User Story' found"
        })

if __name__ == '__main__':
    app.run(port=5001)
