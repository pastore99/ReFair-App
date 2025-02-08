import pandas as pd

class TaskPreprocessor:
    def __init__(self, glove_vectors):
        self.glove_vectors = glove_vectors

    def preprocess(self, text):
        """
        Converts input text into an averaged GloVe embedding vector

        :param text: The input text to be vectorized
        :return: numpy.ndarray: A 2D array (1 row, 100 columns) containing the averaged word embedding.
                      If no words are found in GloVe, returns a zero vector.
        """
        words = text.split()
        vecs = [self.glove_vectors[word] for word in words if word in self.glove_vectors]

        if vecs:
            vec_avg = sum(vecs) / len(vecs)
        else:
            vec_avg = [0] * 100  # Se nessuna parola è in GloVe, vettore nullo

        traindata = pd.DataFrame([vec_avg])
        traindata.columns = traindata.columns.astype(str)
        return traindata.values
