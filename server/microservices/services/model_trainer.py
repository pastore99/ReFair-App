import os
import pickle
import numpy as np
import pandas as pd
from transformers import BertTokenizer
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.base import clone
import gensim
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np


class ModelTrainer:
    def __init__(self, domain_model_path, task_model_path, dataset_path, glove_path):
        self.domain_model_path = domain_model_path
        self.task_model_path = task_model_path
        self.dataset_path = dataset_path
        self.glove_vectors = gensim.models.KeyedVectors.load_word2vec_format(glove_path, binary=False, no_header=True)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def compute_feature_vector(self, user_story):
        """
        Converts a user story into a numerical feature vector using GloVe embeddings.

        :param user_story: The input user story as a string.
        :return: A 100-dimensional feature vector (numpy array).
        """
        words = user_story.split()
        vecs = [self.glove_vectors[word] for word in words if word in self.glove_vectors]
        return np.mean(vecs, axis=0) if vecs else np.zeros(100)

    def retrain_domain_model(self, feedback_list):
        """
        Retrains the domain classification model using both original data and user feedback.

        :param feedback_list: List of user feedback entries, each containing a user story and its predicted domain.
        """
        dataset = pd.read_excel(self.dataset_path)
        unique_domains = dataset["Domain"].unique()

        print("Domini unici nel dataset:", unique_domains)

        X_train, y_train = [], []
        for _, row in dataset.iterrows():
            X_train.append(self.compute_feature_vector(row["User Story"]))
            y_train.append(np.where(unique_domains == row["Domain"])[0][0])

        for entry in feedback_list:
            predicted_domain = entry["predicted_domain"]
            print(f"Predicted domain ricevuto: {predicted_domain}")

            matching_indexes = np.where(unique_domains == predicted_domain)[0]

            if len(matching_indexes) == 0:
                print(f"ERRORE: Il dominio '{predicted_domain}' non esiste nel dataset!")
                continue  # Salta questo feedback

            y_train.append(matching_indexes[0])
            X_train.append(self.compute_feature_vector(entry["user_story"]))

    def retrain_task_model(self, feedback_list):
        """
        Retrains the task classification model using both original dataset and user feedback.

        :param feedback_list: List of user feedback entries, each containing a user story and its predicted tasks.
        """
        dataset = pd.read_excel(self.dataset_path)

        X_train = []
        y_train = []

        mlb = MultiLabelBinarizer()

        for _, row in dataset.iterrows():
            X_train.append(self.compute_feature_vector(row["User Story"]))
            y_train.append(row["Machine Learning Task"].split(','))

        for entry in feedback_list:
            X_train.append(self.compute_feature_vector(entry["user_story"]))
            y_train.append(entry["predicted_tasks"])

        y_train = mlb.fit_transform(y_train)
        X_train = np.array(X_train, dtype=np.float32)
        with open(self.task_model_path, 'rb') as f:
            task_model = pickle.load(f)

        new_model = clone(task_model)
        new_model.fit(X_train, y_train)

        with open(self.task_model_path, 'wb') as f:
            pickle.dump(new_model, f)
        print("Modello dei task aggiornato!")

