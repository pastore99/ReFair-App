from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import BertTokenizer
import pickle
import pandas as pd

import os

# Configurazione Flask
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# Caricamento del modello e del tokenizer
domain_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, '..', 'refair-server', 'models', 'XGBClassifier.pkl')
with open(model_path, 'rb') as f:
    domain_classifier = pickle.load(f)

# Dataset con i domini
user_path = os.path.join(base_dir, '..', 'refair-server', 'datasets', 'Synthetic User Stories.xlsx')
dataset = pd.read_excel(user_path)

@app.route('/predict/domain', methods=['POST'])
def predict_domain():
    """
    Predice il dominio di una user story.
    """
    if not request.is_json:
        return jsonify({
            "status": "failure",
            "motivation": "Request body must be JSON"
        })

    # Estrae la user story dal corpo della richiesta
    data = request.get_json()
    user_story = data.get('user_story')

    if not user_story:
        return jsonify({
            "status": "failure",
            "motivation": "Missing 'user_story' in request"
        })

    # Tokenizzazione e predizione
    tokenized_data = domain_tokenizer([user_story], padding='max_length', max_length=100, truncation=True)
    traindata = pd.DataFrame(tokenized_data['input_ids'])
    traindata.columns = traindata.columns.astype(str)
    prediction = domain_classifier.predict(traindata)

    domain = dataset["Domain"].unique()[prediction[0]]

    return jsonify({
        "status": "success",
        "domain": domain
    })

if __name__ == '__main__':
    app.run(port=5002)