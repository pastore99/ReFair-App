import os
import gensim
import pickle
import pandas as pd

class TaskModelService:
    def __init__(self):
        """
        load modal from extract features
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Caricamento GloVe
        glove_path = os.path.join(base_dir, '..', '..', 'utils', 'models', 'glove.6B.100d.txt')
        if not os.path.exists(glove_path):
            raise FileNotFoundError(f"GloVe model file not found: {glove_path}")
        self.glove_vectors = gensim.models.KeyedVectors.load_word2vec_format(glove_path, binary=False, no_header=True)

        # Caricamento modello di predizione
        mlb_path = os.path.join(base_dir, '..', '..', 'utils', 'models', 'multilabel.pkl')
        svc_path = os.path.join(base_dir, '..', '..', 'utils', 'models', 'LinearSVC_LabelPowerset.pkl')

        if not os.path.exists(mlb_path) or not os.path.exists(svc_path):
            raise FileNotFoundError("One or more model files are missing")

        with open(mlb_path, 'rb') as f:
            self.mlb = pickle.load(f)

        with open(svc_path, 'rb') as f:
            self.lsvc = pickle.load(f)

    def predict_task(self, vectorized_text):
        """
        Predict tasks from vectorized text

        :param vectorized_text: domain and tasks vectorized
        :return: features extracted
        """
        raw_pred = self.lsvc.predict(vectorized_text)
        inv_pred = self.mlb.inverse_transform(raw_pred)  # Output: [('task1', 'task2'), ('task3', 'task4')]
        flat_tasks = [task for tasks_tuple in inv_pred for task in tasks_tuple]
        return flat_tasks  # Output: ['task1', 'task2', 'task3', 'task4']
