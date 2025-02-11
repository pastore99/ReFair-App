from flask import Flask, jsonify, request
from flask_cors import CORS
from services.task_model_service import TaskModelService
from services.task_preprocessor import TaskPreprocessor
from services.task_dataset_service import TaskDatasetService
import traceback
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# Dependency Injection
model_service = TaskModelService()
preprocessor = TaskPreprocessor(model_service.glove_vectors)
dataset_service = TaskDatasetService()

#@app.route('/predict/tasks', methods=['POST'])
# def predict_tasks():
#     """
#     Get tasks from user story and its domain.
#
#     request:
#         json like
#         {
#             "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
#             "domain": "Cardiology"
#         }
#
#     response:
#         json like
#         {
#             "status": "success",
#             "tasks": ["classification", "ranking"],
#             "tasks_features": {
#                 "classification": ["race", "age", "sex"],
#                 "ranking": ["race", "age", "sex"]
#             }
#         }
#     """
#     if not request.is_json:
#         return jsonify({"status": "failure", "motivation": "Request body must be JSON"})
#
#     data = request.get_json()
#     user_story = data.get('user_story')
#     domain = data.get('domain')
#
#     if not user_story or not domain:
#         return jsonify({"status": "failure", "motivation": "Missing 'user_story' or 'domain' in request"})
#
#     try:
#         vectorized_text = preprocessor.preprocess(user_story)
#         predicted_tasks = model_service.predict_task(vectorized_text)
#         ml_tasks = dataset_service.get_tasks_for_domain(domain, predicted_tasks)
#         tasks_features = dataset_service.extract_features(domain, ml_tasks)
#
#         return jsonify({"status": "success", "tasks": ml_tasks, "tasks_features": tasks_features})
#
#     except Exception as e:
#         return jsonify({"status": "failure", "motivation": str(e)}), 500




@app.route('/predict/tasks', methods=['POST'])
def predict_tasks():
    try:
        if not request.is_json:
            return jsonify({"status": "failure", "motivation": "Request body must be JSON"}), 400

        data = request.get_json()
        user_story = data.get('user_story')
        domain = data.get('domain')

        if not user_story or not domain:
            return jsonify({"status": "failure", "motivation": "Missing 'user_story' or 'domain' in request"}), 400

        vectorized_text = preprocessor.preprocess(user_story)
        predicted_tasks = model_service.predict_task(vectorized_text)
        ml_tasks = dataset_service.get_tasks_for_domain(domain, predicted_tasks)
        tasks_features = dataset_service.extract_features(domain, ml_tasks)

        return jsonify({"status": "success", "tasks": ml_tasks, "tasks_features": tasks_features})

    except Exception as e:
        error_details = traceback.format_exc()
        print(error_details)  # Stampa i dettagli dell'errore sulla console
        return jsonify({"status": "failure", "motivation": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5003)
