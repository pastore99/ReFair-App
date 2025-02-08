from flask import Flask, jsonify, request
from flask_cors import CORS
from services.feedback_manager import FeedbackManager
from services.model_trainer import ModelTrainer
import os

app = Flask(__name__)
CORS(app)

# Configurazione percorsi
base_dir = os.path.dirname(os.path.abspath(__file__))
DOMAIN_MODEL_PATH = os.path.join(base_dir, '..', 'utils', 'models', 'XGBClassifier.pkl')
TASK_MODEL_PATH = os.path.join(base_dir, '..', 'utils', 'models', 'LinearSVC_LabelPowerset.pkl')
DATASET_PATH = os.path.join(base_dir, '..', 'utils', 'datasets', 'Synthetic User Stories.xlsx')
GLOVE_PATH = os.path.join(base_dir, '..', 'utils', 'models', 'glove.6B.100d.txt')

# Inizializza il trainer
model_trainer = ModelTrainer(DOMAIN_MODEL_PATH, TASK_MODEL_PATH, DATASET_PATH, GLOVE_PATH)

# Inizializza i gestori di feedback
domain_feedback_manager = FeedbackManager(os.path.join(base_dir, '..', 'utils', 'feedback_results', 'domain_feedbacks.json'), 10, model_trainer.retrain_domain_model)
task_feedback_manager = FeedbackManager(os.path.join(base_dir, '..', 'utils', 'feedback_results', 'tasks_feedbacks.json'), 10, model_trainer.retrain_task_model)

@app.route('/feedback/domain', methods=['POST'])
def feedback_domain():
    """
    Store feedback user for a prediction domain result and retrain modal of domain predict.

    request:
        {
            "user_story": "As an orthopedic surgeon, I want to review X-ray images to identify bone fractures quickly.",
            "predicted_domain": "orthopedics",
            "feedback_value": 4
        }

    response:
        json ack
    """
    data = request.get_json()
    domain_feedback_manager.save_feedback(data)
    return jsonify({"status": "success", "message": "Domain feedback received"}), 200

@app.route('/feedback/tasks', methods=['POST'])
def feedback_tasks():
    """
    Store feedback user for a prediction tasks result and retrain modal of tasks predict.

    request:
        {
            "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
            "domain": "cardiology",
            "predicted_tasks": ["Identify Multiword Expressions", "Risk Factor Analysis"],
            "feedback_value": 5
        }

    response:
        json ack
    """
    data = request.get_json()
    task_feedback_manager.save_feedback(data)
    return jsonify({"status": "success", "message": "Task feedback received"}), 200

if __name__ == '__main__':
    app.run(port=5005)
