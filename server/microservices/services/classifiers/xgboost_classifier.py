from .abstract_classifier import AbstractClassifier
import pandas as pd
import os
import pickle
from transformers import BertTokenizer

class XGBoostDomainClassifier(AbstractClassifier):
    """
    XGBoost classifier to predict domain
    """

    def __init__(self):
        """
        Main class to load XGB model
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, '..','..', '..', 'utils', 'models', 'XGBClassifier.pkl')

        with open(model_path, 'rb') as f:
            self.domain_classifier = pickle.load(f)

        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        # Caricamento dataset per estrarre i domini
        user_path = os.path.join(base_dir, '..', '..', '..', 'utils', 'datasets', 'Synthetic User Stories.xlsx')
        self.dataset = pd.read_excel(user_path)

    def predict(self, user_story: str):
        """
        Predict domain

        :argument
            user_story: the user story to predict domain
        """
        tokenized_data = self.tokenizer([user_story], padding='max_length', max_length=100, truncation=True)
        traindata = pd.DataFrame(tokenized_data['input_ids'])
        traindata.columns = traindata.columns.astype(str)
        prediction = self.domain_classifier.predict(traindata)

        return self.dataset["Domain"].unique()[prediction[0]]