import os
import json
from datetime import datetime
import numpy as np
from flask import jsonify, request
from flask_cors import CORS
import gensim
import pickle
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.base import clone


base_dir = os.path.dirname(os.path.abspath(__file__))

# Caricamento dei modelli e dei dati
# Caricamento di GloVe per ottenere il vettore medio della user story
glove_vectors = gensim.models.KeyedVectors.load_word2vec_format(
    os.path.join(base_dir, '..', '..', 'refair-server', 'models', 'glove.6B.100d.txt'),
    binary=False,
    no_header=True
)

# Caricamento del MultiLabelBinarizer e del classificatore (es. LinearSVC con LabelPowerset)
with open(os.path.join(base_dir, '..', '..', 'refair-server', 'models', 'multilabel.pkl'), 'rb') as f:
    mlb = pickle.load(f)

with open(os.path.join(base_dir, '..', '..', 'refair-server', 'models', 'LinearSVC_LabelPowerset.pkl'), 'rb') as f:
    lsvc = pickle.load(f)

# Caricamento dei mapping per dominio e task
domain_task_mapping = pd.read_csv(os.path.join(base_dir, '..', '..', 'refair-server', 'datasets', 'domains-tasks-mapping.csv'))
domains_mapping = pd.read_csv(os.path.join(base_dir, '..', '..', 'refair-server', 'datasets', 'domains-features-mapping.csv'))
tasks_mapping = pd.read_csv(os.path.join(base_dir, '..', '..', 'refair-server', 'datasets', 'tasks-features-mapping.csv'))

# ====================================================
# Costanti per il salvataggio dei feedback e del dataset originale
# ====================================================
FEEDBACK_FILE = os.path.join(base_dir, '..', '..', 'feedback_results', 'tasks_feedbacks.json')
# Se hai un file JSON per il dataset originale lo usi, altrimenti useremo l'excel
# ORIGINAL_DATASET_FILE = 'original_dataset.json'
EXCEL_DATASET_FILE = os.path.join(base_dir, '..', '..', 'refair-server', 'datasets', 'Synthetic User Stories.xlsx')
# Imposta la soglia di feedback per attivare il retraining (modifica secondo le necessità)
FEEDBACK_THRESHOLD = 10

# Funzioni per il salvataggio del feedback e per il retraining
def save_feedback(entry):
    """Salva l'entry del feedback nel file JSON."""
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            try:
                feedback_list = json.load(f)
            except json.JSONDecodeError:
                feedback_list = []
    else:
        feedback_list = []
    feedback_list.append(entry)
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_list, f)

def load_original_dataset():
    """
    Carica il dataset originale dal file Excel.
    Il file Excel deve contenere le colonne:
      - Domain Cluster
      - Topic
      - Domain
      - Machine Learning Task
      - User Story
    Per ogni riga vengono estratti 'User Story', 'Domain' e 'Machine Learning Task'.
    """
    if os.path.exists(EXCEL_DATASET_FILE):
        try:
            df = pd.read_excel(EXCEL_DATASET_FILE)
        except Exception as e:
            print("Errore nel caricamento del dataset Excel:", e)
            return []

        dataset = []
        for index, row in df.iterrows():
            user_story = row.get("User Story")
            domain = row.get("Domain")
            ml_task = row.get("Machine Learning Task")
            if pd.isna(user_story) or pd.isna(domain) or pd.isna(ml_task):
                continue  # Salta righe incomplete
            # Se la colonna Machine Learning Task contiene più task separati da virgola, trasformali in lista
            if isinstance(ml_task, str):
                tasks = [t.strip() for t in ml_task.split(',')]
            else:
                tasks = [ml_task]
            dataset.append({
                "user_story": user_story,
                "domain": domain,
                "predicted_tasks": tasks
            })
        return dataset
    else:
        print("File Excel del dataset originale non trovato.")
        return []

def compute_feature_vector(user_story):
    """Calcola il vettore medio per la user_story utilizzando glove_vectors."""
    words = user_story.split()
    vecs = [glove_vectors[word] for word in words if word in glove_vectors]
    return sum(vecs) / len(vecs) if vecs else [0] * 100

def retrain_model(feedback_list):
    global lsvc  # Dichiarazione globale all'inizio della funzione

    """
    Pipeline di retraining combinato:
      1. Carica il dataset originale dal file Excel e converte ciascun campione in (X, y) con peso fisso.
      2. Converte i feedback in esempi di training con peso pari al feedback_value.
      3. Unisce i dataset e, tramite resampling ponderato, addestra un nuovo modello (clonando quello attuale).
      4. Valuta il nuovo modello con F1-score (ponderato) sul dataset combinato.
      5. Se il nuovo modello performa meglio, lo salva in produzione.
    """
    X_feedback = []
    y_feedback = []
    weights_feedback = []

    # Processa i dati di feedback
    for entry in feedback_list:
        vec_avg = compute_feature_vector(entry['user_story'])
        X_feedback.append(vec_avg)
        # Trasforma le task predette in un vettore binario
        binary_label = mlb.transform([entry['predicted_tasks']])[0]
        y_feedback.append(binary_label)
        weights_feedback.append(float(entry['feedback_value']))

    X_feedback = np.array(X_feedback)
    y_feedback = np.array(y_feedback)

    # Carica e processa il dataset originale dall'Excel
    original_data = load_original_dataset()
    X_original = []
    y_original = []
    weights_original = []

    for entry in original_data:
        vec_avg = compute_feature_vector(entry['user_story'])
        X_original.append(vec_avg)
        # Trasforma le task in un vettore binario
        binary_label = mlb.transform([entry['predicted_tasks']])[0]
        y_original.append(binary_label)
        # Peso fisso per i dati originali (es. 1.0)
        weights_original.append(1.0)

    X_original = np.array(X_original)
    y_original = np.array(y_original)

    # Combina i dataset: originale + feedback
    if X_original.size and X_feedback.size:
        X_combined = np.concatenate([X_original, X_feedback], axis=0)
        y_combined = np.concatenate([y_original, y_feedback], axis=0)
        weights_combined = np.concatenate([np.array(weights_original), np.array(weights_feedback)], axis=0)
    elif X_original.size:
        X_combined = X_original
        y_combined = y_original
        weights_combined = np.array(weights_original)
    elif X_feedback.size:
        X_combined = X_feedback
        y_combined = y_feedback
        weights_combined = np.array(weights_feedback)
    else:
        print("Nessun dato disponibile per il retraining.")
        return

    # Valutazione del modello attuale sul dataset combinato
    try:
        old_predictions = lsvc.predict(X_combined)
        old_f1 = f1_score(y_combined, old_predictions, average='micro', sample_weight=weights_combined)
    except Exception as e:
        print("Errore nella valutazione del modello attuale:", e)
        old_f1 = 0

    # Clona il modello attuale
    new_model = clone(lsvc)

    # Implementiamo il resampling ponderato:
    # Per ogni campione, replicalo int(round(peso)) volte.
    X_weighted = []
    y_weighted = []
    for i, w in enumerate(weights_combined):
        reps = int(round(w))  # Supponiamo che w sia un intero o vicino a un intero
        for _ in range(reps):
            X_weighted.append(X_combined[i])
            y_weighted.append(y_combined[i])
    X_weighted = np.array(X_weighted)
    y_weighted = np.array(y_weighted)

    try:
        new_model.fit(X_weighted, y_weighted)
    except Exception as e:
        print("Errore nel retraining del modello:", e)
        return

    try:
        new_predictions = new_model.predict(X_combined)
        new_f1 = f1_score(y_combined, new_predictions, average='micro', sample_weight=weights_combined)
    except Exception as e:
        print("Errore nella valutazione del nuovo modello:", e)
        new_f1 = 0

    print("Valutazione modello attuale (F1):", old_f1)
    print("Valutazione nuovo modello (F1):", new_f1)

    # Se il nuovo modello performa meglio, sostituisci quello in produzione
    if new_f1 > old_f1:
        lsvc = new_model
        model_path = os.path.join(base_dir, '..', '..', 'refair-server', 'models', 'LinearSVC_LabelPowerset.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(lsvc, f)
        print("Modello aggiornato e salvato con successo.")
        # Svuota il file dei feedback (oppure archivialo, se necessario)
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump([], f)
    else:
        print("Il nuovo modello non è migliore. Nessun aggiornamento effettuato.")

def check_feedback_threshold_and_retrain():
    """Controlla se il numero di feedback supera la soglia e, in tal caso, avvia il retraining."""
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            try:
                feedback_list = json.load(f)
            except json.JSONDecodeError:
                feedback_list = []
        if len(feedback_list) >= FEEDBACK_THRESHOLD:
            print("Soglia di feedback raggiunta. Avvio del retraining...")
            retrain_model(feedback_list)

def get_tasks_feedback():
    """
    Riceve il feedback come valore numerico (da 1 a 5) insieme ai dati della richiesta e lo salva.
    Esempio di payload JSON:
    {
        "user_story": "La storia dell'utente ...",
        "domain": "nome_del_dominio",
        "predicted_tasks": ["task1", "task2"],
        "feedback_value": 4
    }
    """
    if not request.is_json:
        return jsonify({"status": "failure", "motivation": "Request body must be JSON"}), 400

    data = request.get_json()
    required_fields = ['user_story', 'domain', 'predicted_tasks', 'feedback_value']
    for field in required_fields:
        if field not in data:
            return jsonify({"status": "failure", "motivation": f"Missing field: {field}"}), 400

    try:
        feedback_value = float(data['feedback_value'])
        if feedback_value < 1 or feedback_value > 5:
            return jsonify({"status": "failure", "motivation": "feedback_value must be between 1 and 5"}), 400
    except ValueError:
        return jsonify({"status": "failure", "motivation": "feedback_value must be numeric"}), 400

    feedback_entry = {
        "user_story": data['user_story'],
        "domain": data['domain'],
        "predicted_tasks": data['predicted_tasks'],
        "feedback_value": feedback_value,
        "timestamp": datetime.now().isoformat()
    }

    save_feedback(feedback_entry)
    # Controlla se la soglia per il retraining è stata raggiunta
    check_feedback_threshold_and_retrain()

    return jsonify({"status": "success", "message": "Feedback received"}), 200