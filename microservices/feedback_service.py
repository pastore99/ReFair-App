import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import gensim
import pickle
import pandas as pd
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# Percorso dei file di modello e dataset
GLOVE_PATH = '../refair-server/models/glove.6B.100d.txt'
MLB_PATH = '../refair-server/models/multilabel.pkl'
LSVC_PATH = '../refair-server/models/LinearSVC_LabelPowerset.pkl'
DOMAIN_TASK_MAPPING_PATH = '../refair-server/datasets/domains-tasks-mapping.csv'
DOMAINS_MAPPING_PATH = '../refair-server/datasets/domains-features-mapping.csv'
TASKS_MAPPING_PATH = '../refair-server/datasets/tasks-features-mapping.csv'

# Caricamento dei modelli e dei dati
glove_vectors = gensim.models.KeyedVectors.load_word2vec_format(GLOVE_PATH, binary=False, no_header=True)

with open(MLB_PATH, 'rb') as f:
    mlb = pickle.load(f)

with open(LSVC_PATH, 'rb') as f:
    lsvc = pickle.load(f)

domain_task_mapping = pd.read_csv(DOMAIN_TASK_MAPPING_PATH)
domains_mapping = pd.read_csv(DOMAINS_MAPPING_PATH)
tasks_mapping = pd.read_csv(TASKS_MAPPING_PATH)

def intersection(lst1, lst2):
    """Ritorna l'intersezione tra due liste."""
    return [value for value in lst1 if value in lst2]

def get_ml_task(user_story, domain):
    """
    Predice i task ML da una user story e filtra i task rilevanti per il dominio.
    """
    traindata = []
    for msg in [user_story]:
        words = msg.split()
        vecs = []
        for word in words:
            if word in glove_vectors:
                vecs.append(glove_vectors[word])
        if vecs:
            vec_avg = sum(vecs) / len(vecs)
        else:
            vec_avg = [0] * 100
        traindata.append(vec_avg)
    traindata = pd.DataFrame(traindata)
    traindata.columns = traindata.columns.astype(str)

    output = []
    for prediction in mlb.inverse_transform(lsvc.predict(traindata.values))[0]:
        for index in domain_task_mapping.index:
            if (domain_task_mapping['Domain'][index].lower() == domain.lower() and
                    domain_task_mapping['Task'][index].lower() == prediction.lower()):
                output.append(prediction)
    return output

def feature_extraction(domain, mltasks):
    """
    Estrae le feature sensibili rilevanti per il dominio e i task ML.
    """
    out_features = {}

    # Feature del dominio
    domain_features = []
    for index in domains_mapping.index:
        if domains_mapping['Domain'][index].lower() == domain.lower():
            domain_features.append(domains_mapping['Feature'][index])

    # Feature per ogni task
    for task in mltasks:
        tmp = []
        for index in tasks_mapping.index:
            if tasks_mapping['Task'][index].lower() == task.lower():
                tmp.append(tasks_mapping['Feature'][index])
        out_features[task] = intersection(tmp, domain_features)

    return out_features

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """
    Gestisce il feedback e aggiorna il modello in tempo reale.
    """
    data = request.json

    if not data.get('resultId') or not data.get('rating') or not data.get('user_story') or not data.get('domain'):
        return jsonify({"error": "Invalid data. 'resultId', 'rating', 'user_story', and 'domain' are required."}), 400

    feedback = {
        "feedbackId": str(datetime.utcnow().timestamp()),
        "resultId": data['resultId'],
        "rating": data['rating'],
        "user_story": data['user_story'],
        "domain": data['domain'],
        "timestamp": datetime.utcnow().isoformat(),
        "userId": data.get('userId')
    }

    # Predizione dei task ML e feature rilevanti
    ml_tasks = get_ml_task(feedback['user_story'], feedback['domain'])
    tasks_features = feature_extraction(feedback['domain'], ml_tasks)

    # Aggiorna il modello con il feedback
    try:
        # Usa la user story come input e il rating (o una label derivata) come output
        input_features = extract_features(feedback['user_story'])  # Funzione per convertire la user story in feature vettoriali
        correct_label = feedback['rating']  # Puoi adattare questo per essere più significativo (es. una label derivata)

        update_model(input_features, correct_label)  # Aggiorna il modello

        print("Model updated successfully with feedback.")
    except Exception as e:
        print(f"Error updating the model: {str(e)}")

    # Salva il feedback nel file JSON
    try:
        with open("feedback.json", "r") as f:
            feedback_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        feedback_data = []

    feedback_data.append(feedback)

    with open("feedback.json", "w") as f:
        json.dump(feedback_data, f, indent=4)

    return jsonify({
        "message": "Feedback processed successfully and model updated",
        "tasks": ml_tasks,
        "tasks_features": tasks_features,
        "feedback": feedback
    }), 201


@app.route('/predict/tasks', methods=['POST'])
def predict_tasks():
    """
    Predice i task ML e le feature sensibili da una user story e un dominio.
    """
    if not request.is_json:
        return jsonify({
            "status": "failure",
            "motivation": "Request body must be JSON"
        })

    # Estrai user story e dominio dal corpo della richiesta
    data = request.get_json()
    user_story = data.get('user_story')
    domain = data.get('domain')

    if not user_story or not domain:
        return jsonify({
            "status": "failure",
            "motivation": "Missing 'user_story' or 'domain' in request"
        })

    # Predizione dei task e delle feature
    ml_tasks = get_ml_task(user_story, domain)
    tasks_features = feature_extraction(domain, ml_tasks)

    return jsonify({
        "status": "success",
        "tasks": ml_tasks,
        "tasks_features": tasks_features
    })

def update_model(input_features, correct_label):
    """
    Aggiorna il modello con i dati forniti.
    """
    # Carica il modello salvato
    with open("../refair-server/models/multilabel.pkl", "rb") as f:
        model = pickle.load(f)

    # Esegui l'aggiornamento del modello (incrementale)
    model.partial_fit([input_features], [correct_label])

    # Salva il modello aggiornato
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Model updated and saved successfully.")

def extract_features(user_story):
    """
    Estrae il vettore di feature da una user story utilizzando GloVe.

    Args:
        user_story (str): La user story da convertire in un vettore.

    Returns:
        list: Il vettore di feature ottenuto mediando i vettori delle parole presenti nella user story.
    """
    words = user_story.split()  # Divide il testo in parole
    vecs = []

    # Itera su ogni parola e controlla se è presente nel vocabolario di GloVe
    for word in words:
        if word in glove_vectors:  # `glove_vectors` è il modello caricato
            vecs.append(glove_vectors[word])

    # Calcola la media dei vettori delle parole
    if vecs:
        vec_avg = sum(vecs) / len(vecs)
    else:
        # Se nessuna parola è valida, restituisce un vettore di zeri
        vec_avg = [0] * glove_vectors.vector_size

    return vec_avg

if __name__ == '__main__':
    if not os.path.exists(GLOVE_PATH) or not os.path.exists(MLB_PATH) or not os.path.exists(LSVC_PATH):
        raise FileNotFoundError("One or more model files are missing. Ensure all model files are present.")

    app.run(debug=True, host="0.0.0.0", port=5005)
