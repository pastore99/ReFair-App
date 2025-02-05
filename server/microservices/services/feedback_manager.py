import os
import json
from datetime import datetime

class FeedbackManager:
    def __init__(self, feedback_file, feedback_threshold, retrain_callback):
        self.feedback_file = feedback_file
        self.feedback_threshold = feedback_threshold
        self.retrain_callback = retrain_callback  # Callback per avviare il retraining

    def save_feedback(self, entry):
        """
        Save feedback in json file.

        :param entry: json feedback to save
        :return: if json file has ten entry, the method call retraining method and update the model, else a json ack.
        """
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r') as f:
                try:
                    feedback_list = json.load(f)
                except json.JSONDecodeError:
                    feedback_list = []
        else:
            feedback_list = []

        entry["timestamp"] = datetime.now().isoformat()
        feedback_list.append(entry)

        with open(self.feedback_file, 'w') as f:
            json.dump(feedback_list, f, indent=4, ensure_ascii=False)

        # Controlla se è il momento di riaddestrare il modello
        if len(feedback_list) >= self.feedback_threshold:
            print("Soglia di feedback raggiunta. Avvio del retraining...")
            self.retrain_callback(feedback_list)
