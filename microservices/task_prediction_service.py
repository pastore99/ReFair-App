from flask import Flask, jsonify, request
from flask_cors import CORS
import gensim
import pickle
import pandas as pd

# Configurazione Flask
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# Caricamento dei modelli e dei dati
glove_vectors = gensim.models.KeyedVectors.load_word2vec_format('../refair-server/models/glove.6B.100d.txt', binary=False, no_header=True)

with open('../refair-server/models/multilabel.pkl', 'rb') as f:
    mlb = pickle.load(f)

with open('../refair-server/models/LinearSVC_LabelPowerset.pkl', 'rb') as f:
    lsvc = pickle.load(f)

domain_task_mapping = pd.read_csv("../refair-server/datasets/domains-tasks-mapping.csv")
domains_mapping = pd.read_csv("../refair-server/datasets/domains-features-mapping.csv")
tasks_mapping = pd.read_csv("../refair-server/datasets/tasks-features-mapping.csv")

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
    # aggiungere controllo per prendere domain in input se presente altrimenti si fa get_domain

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

if __name__ == '__main__':
    app.run(port=5003)
