import json
from .classifiers.xgboost_classifier import XGBoostDomainClassifier
from .classifiers.bert_classifier import BERTDomainClassifier

class ClassifierFactory:
    """
    Factory class to get correct classifier.
    """

    @staticmethod
    def get_domain_classifier():
        """
        Get the classifier from a config.json file
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
            algorithm = config.get("default_algorithm", "xgboost")
        except FileNotFoundError:
            algorithm = "xgboost"  # Default se il file non esiste

        if algorithm == "bert":
            return BERTDomainClassifier()
        return XGBoostDomainClassifier()