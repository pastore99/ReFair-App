import os
import json
import pickle
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import BertTokenizer
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.base import clone

# Configurazione Flask
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# Percorsi dei file
ORIGINAL_DOMAIN_DATASET_FILE = "../refair-server/datasets/Synthetic User Stories.xlsx"
DOMAIN_FEEDBACK_FILE = "domain_feedbacks.json"
DOMAIN_FEEDBACK_THRESHOLD = 10

# Caricamento del tokenizer e del modello
domain_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
with open('../refair-server/models/XGBClassifier.pkl', 'rb') as f:
    domain_classifier = pickle.load(f)

# Caricamento del dataset originale (usato per mappare l'indice al dominio nella predizione)
# Questo dataset viene usato per l'endpoint di predizione per estrarre i domini unici.
dataset = pd.read_excel(ORIGINAL_DOMAIN_DATASET_FILE)

# --- FUNZIONI DI FEATURE EXTRACTION ---

def compute_domain_features(user_story):
    """
    Tokenizza la user story con il tokenizer BERT, usando max_length=101,
    e restituisce un vettore numpy contenente gli input_ids.
    """
    tokenized = domain_tokenizer(
        [user_story],
        padding='max_length',
        max_length=101,  # Assicuriamoci di avere 101 feature, come nel training
        truncation=True
    )
    return np.array(tokenized['input_ids'][0])

# --- FUNZIONI PER IL FEEDBACK ---

def save_domain_feedback(entry):
    """Salva un feedback relativo alla predizione del dominio in DOMAIN_FEEDBACK_FILE."""
    if os.path.exists(DOMAIN_FEEDBACK_FILE):
        with open(DOMAIN_FEEDBACK_FILE, 'r') as f:
            try:
                feedback_list = json.load(f)
            except json.JSONDecodeError:
                feedback_list = []
    else:
        feedback_list = []
    feedback_list.append(entry)
    with open(DOMAIN_FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_list, f)

def load_domain_feedback():
    """Carica e restituisce la lista dei feedback salvati."""
    if os.path.exists(DOMAIN_FEEDBACK_FILE):
        with open(DOMAIN_FEEDBACK_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def check_domain_feedback_threshold_and_retrain():
    """Controlla se il numero dei feedback raggiunge la soglia e, in tal caso, avvia il retraining."""
    feedback_list = load_domain_feedback()
    if len(feedback_list) >= DOMAIN_FEEDBACK_THRESHOLD:
        print("Soglia di feedback domain raggiunta. Avvio del retraining...")
        retrain_domain_model(feedback_list)

# --- PIPELINE DI RETRAINING PER IL DOMAIN CLASSIFIER ---

def retrain_domain_model(feedback_list):
    global domain_classifier
    # Carichiamo il dataset originale dal file Excel
    original_df = pd.read_excel(ORIGINAL_DOMAIN_DATASET_FILE)
    # Otteniamo l'elenco dei domini unici (l'ordine deve rimanere costante)
    unique_domains = original_df["Domain"].unique()

    # Costruiamo il dataset originale
    X_original = []
    y_original = []
    weights_original = []
    for idx, row in original_df.iterrows():
        user_story = row["User Story"]
        domain = row["Domain"]
        X_original.append(compute_domain_features(user_story))
        # Convertiamo il dominio in un'etichetta numerica basata su unique_domains
        label = np.where(unique_domains == domain)[0][0]
        y_original.append(label)
        weights_original.append(1.0)  # Peso fisso per i dati originali
    X_original = np.array(X_original)
    y_original = np.array(y_original)
    weights_original = np.array(weights_original)

    # Costruiamo il dataset dai feedback
    X_feedback = []
    y_feedback = []
    weights_feedback = []
    for entry in feedback_list:
        user_story = entry["user_story"]
        predicted_domain = entry["predicted_domain"]
        try:
            # Convertiamo il predicted_domain in etichetta; se non presente saltiamo il feedback
            label = np.where(unique_domains == predicted_domain)[0][0]
        except IndexError:
            continue
        # Aggiungiamo il campione solo se il dominio è riconosciuto
        X_feedback.append(compute_domain_features(user_story))
        y_feedback.append(label)
        weights_feedback.append(float(entry["feedback_value"]))

    if len(X_feedback) > 0:
        X_feedback = np.array(X_feedback)
        y_feedback = np.array(y_feedback)
        weights_feedback = np.array(weights_feedback)
    else:
        X_feedback = np.empty((0, 101))  # 101 feature
        y_feedback = np.array([])
        weights_feedback = np.array([])

    # Combiniamo i dataset originali e i feedback
    if X_feedback.shape[0] > 0:
        X_combined = np.concatenate([X_original, X_feedback], axis=0)
        y_combined = np.concatenate([y_original, y_feedback], axis=0)
        weights_combined = np.concatenate([weights_original, weights_feedback], axis=0)
    else:
        X_combined = X_original
        y_combined = y_original
        weights_combined = weights_original

    # Valutazione del modello attuale sul dataset combinato
    try:
        old_preds = domain_classifier.predict(X_combined)
        old_accuracy = accuracy_score(y_combined, old_preds, sample_weight=weights_combined)
    except Exception as e:
        print("Errore nella valutazione del modello attuale:", e)
        old_accuracy = 0

    # Cloniamo il modello attuale e ritreniamo usando sample_weight
    new_model = clone(domain_classifier)
    try:
        new_model.fit(X_combined, y_combined, sample_weight=weights_combined)
    except Exception as e:
        print("Errore nel retraining del modello domain:", e)
        return
    try:
        new_preds = new_model.predict(X_combined)
        new_accuracy = accuracy_score(y_combined, new_preds, sample_weight=weights_combined)
    except Exception as e:
        print("Errore nella valutazione del nuovo modello domain:", e)
        new_accuracy = 0

    print("Accuratezza modello attuale:", old_accuracy)
    print("Accuratezza nuovo modello:", new_accuracy)

    # Se il nuovo modello migliora, lo salviamo in produzione e svuotiamo i feedback
    if new_accuracy > old_accuracy:
        domain_classifier = new_model
        model_path = '../refair-server/models/XGBClassifier.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(domain_classifier, f)
        print("Domain classifier aggiornato e salvato con successo.")
        with open(DOMAIN_FEEDBACK_FILE, 'w') as f:
            json.dump([], f)
    else:
        print("Il nuovo domain classifier non è migliore. Nessun aggiornamento effettuato.")

# --- ENDPOINT DI PREDIZIONE ---

@app.route('/predict/domain', methods=['POST'])
def predict_domain():
    """
    Predice il dominio di una user story.
    Il JSON in input deve contenere la chiave "user_story".
    """
    if not request.is_json:
        return jsonify({"status": "failure", "motivation": "Request body must be JSON"}), 400
    data = request.get_json()
    user_story = data.get("user_story")
    if not user_story:
        return jsonify({"status": "failure", "motivation": "Missing 'user_story' in request"}), 400

    tokenized_data = domain_tokenizer(
        [user_story],
        padding='max_length',
        max_length=101,  # Utilizziamo 101 token
        truncation=True
    )
    # Creiamo un DataFrame per essere compatibili con il modello addestrato
    traindata = pd.DataFrame(tokenized_data['input_ids'])
    traindata.columns = traindata.columns.astype(str)
    prediction = domain_classifier.predict(traindata.values)
    # Recuperiamo il dominio dalla lista dei domini unici del dataset
    domain = dataset["Domain"].unique()[prediction[0]]
    return jsonify({"status": "success", "domain": domain})

# --- ENDPOINT DI FEEDBACK ---

@app.route('/feedback/domain', methods=['POST'])
def feedback_domain():
    """
    Riceve un feedback per la predizione del dominio.
    Il JSON in input deve contenere:
      - "user_story"
      - "predicted_domain" (il dominio predetto dal sistema)
      - "feedback_value" (un valore numerico da 1 a 5)
    """
    if not request.is_json:
        return jsonify({"status": "failure", "motivation": "Request body must be JSON"}), 400
    data = request.get_json()
    required_fields = ["user_story", "predicted_domain", "feedback_value"]
    for field in required_fields:
        if field not in data:
            return jsonify({"status": "failure", "motivation": f"Missing field: {field}"}), 400
    try:
        feedback_value = float(data["feedback_value"])
        if feedback_value < 1 or feedback_value > 5:
            return jsonify({"status": "failure", "motivation": "feedback_value must be between 1 and 5"}), 400
    except ValueError:
        return jsonify({"status": "failure", "motivation": "feedback_value must be numeric"}), 400

    feedback_entry = {
        "user_story": data["user_story"],
        "predicted_domain": data["predicted_domain"],
        "feedback_value": feedback_value,
        "timestamp": pd.Timestamp.now().isoformat()
    }
    save_domain_feedback(feedback_entry)
    check_domain_feedback_threshold_and_retrain()
    return jsonify({"status": "success", "message": "Domain feedback received"}), 200

if __name__ == '__main__':
    app.run(port=5002)
