from .abstract_classifier import AbstractClassifier

class BERTDomainClassifier(AbstractClassifier):
    """
    BERT classifier to predict domain
    """
    def predict(self, user_story: str):
        """
        Predict domain

        :argument
            user_story: the user story to predict domain
        """
        return "Predizione con BERT (simulata)"