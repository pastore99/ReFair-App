from abc import ABC, abstractmethod

class AbstractClassifier(ABC):
    """
    Abstract interface for classifiers.
    """

    @abstractmethod
    def predict(self, user_story: str):
        """
        Abstract method than every classifiers have to implement.

        :param
            user_story: the user story to analyze

        :return:
            prediction result
        """
        pass