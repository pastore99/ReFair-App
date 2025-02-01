import os
import json
import pickle
import pandas as pd
import numpy as np
from transformers import BertTokenizer
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from copy import deepcopy  # Utilizziamo deepcopy al posto di clone
from flask import jsonify, request

# Configurazioni e percorsi
base_dir = os.path.dirname(os.path.abspath(__file__))
ORIGINAL_DOMAIN_DATASET_FILE = os.path.join(base_dir, '..', '..', 'refair-server', 'datasets', 'Synthetic User Stories.xlsx')
DOMAIN_FEEDBACK_FILE = os.path.join(base_dir, '..', '..', 'feedback_results', 'domain_feedbacks.json')
DOMAIN_FEEDBACK_THRESHOLD = 10

# Carica il tokenizer e il modello
domain_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
with open(os.path.join(base_dir, '..', '..', 'refair-server', 'models', 'XGBClassifier.pkl'), 'rb') as f:
    domain_classifier = pickle.load(f)

# Carica il dataset (per ottenere l'elenco dei domini unici)
dataset = pd.read_excel(ORIGINAL_DOMAIN_DATASET_FILE)

def compute_domain_features(user_story):
    """
    Tokenizza la user story con il tokenizer BERT, usando max_length=100
    (per restituire 100 token, come previsto dal modello) e restituisce
    un vettore numpy contenente gli input_ids.
    """
    tokenized = domain_tokenizer(
        [user_story],
        padding='max_length',
        max_length=100,  # Usa 100 token, per essere coerenti con il training
        truncation=True
    )
    return np.array(tokenized['input_ids'][0])

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

def retrain_domain_model(feedback_list):
    global domain_classifier
    # Carica il dataset originale dal file Excel
    original_df = pd.read_excel(ORIGINAL_DOMAIN_DATASET_FILE)
    # Ottieni l'elenco dei domini unici (l'ordine deve rimanere costante)
    unique_domains = original_df["Domain"].unique()

    # Costruzione del dataset originale
    X_original = []
    y_original = []
    weights_original = []
    for idx, row in original_df.iterrows():
        user_story = row["User Story"]
        domain = row["Domain"]
        X_original.append(compute_domain_features(user_story))
        label = np.where(unique_domains == domain)[0][0]
        y_original.append(label)
        weights_original.append(1.0)  # Peso fisso per i dati originali
    X_original = np.array(X_original)
    y_original = np.array(y_original)
    weights_original = np.array(weights_original)

    # Costruzione del dataset dai feedback
    X_feedback = []
    y_feedback = []
    weights_feedback = []
    for entry in feedback_list:
        user_story = entry["user_story"]
        predicted_domain = entry["predicted_domain"]
        try:
            label = np.where(unique_domains == predicted_domain)[0][0]
        except IndexError:
            continue
        X_feedback.append(compute_domain_features(user_story))
        y_feedback.append(label)
        weights_feedback.append(float(entry["feedback_value"]))
    if len(X_feedback) > 0:
        X_feedback = np.array(X_feedback)
        y_feedback = np.array(y_feedback)
        weights_feedback = np.array(weights_feedback)
    else:
        X_feedback = np.empty((0, 100))  # 100 feature
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

    # --- Patching dell'oggetto domain_classifier ---
    if not hasattr(domain_classifier, "device"):
        setattr(domain_classifier, "device", "cpu")
    if not hasattr(domain_classifier, "multi_strategy"):
        setattr(domain_classifier, "multi_strategy", None)

    # Otteniamo i parametri dal modello patchato
    try:
        params = domain_classifier.get_params()
    except Exception as e:
        print("Errore in get_params:", e)
        return

    # Creiamo un nuovo modello XGBClassifier con gli stessi parametri
    new_model = XGBClassifier(**params)
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

    if new_accuracy > old_accuracy:
        domain_classifier = new_model
        model_path = os.path.join(base_dir, '..', '..', 'refair-server', 'models', 'XGBClassifier.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(domain_classifier, f)
        print("Domain classifier aggiornato e salvato con successo.")
        with open(DOMAIN_FEEDBACK_FILE, 'w') as f:
            json.dump([], f)
    else:
        print("Il nuovo domain classifier non è migliore. Nessun aggiornamento effettuato.")


def check_domain_feedback_threshold_and_retrain():
    feedback_list = load_domain_feedback()
    if len(feedback_list) >= DOMAIN_FEEDBACK_THRESHOLD:
        print("Soglia di feedback domain raggiunta. Avvio del retraining...")
        retrain_domain_model(feedback_list)

def predict_domain_endpoint():
    if not request.is_json:
        return jsonify({"status": "failure", "motivation": "Request body must be JSON"}), 400
    data = request.get_json()
    user_story = data.get("user_story")
    if not user_story:
        return jsonify({"status": "failure", "motivation": "Missing 'user_story' in request"}), 400

    tokenized_data = domain_tokenizer(
        [user_story],
        padding='max_length',
        max_length=100,  # Usa 100 token
        truncation=True
    )
    traindata = pd.DataFrame(tokenized_data['input_ids'])
    traindata.columns = traindata.columns.astype(str)
    prediction = domain_classifier.predict(traindata.values)
    domain = dataset["Domain"].unique()[prediction[0]]
    return jsonify({"status": "success", "domain": domain})

def get_domain_feedback():
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
