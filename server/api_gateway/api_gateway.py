from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# URL dei microservizi
MICROSERVICES = {
    "file_management": "http://localhost:5001",
    "domain_prediction": "http://localhost:5002",
    "task_prediction": "http://localhost:5003",
    "report_generation": "http://localhost:5004",
    "feedback": "http://localhost:5005"
}

@app.route('/storiesload', methods=['POST'])
def stories_load():
    """
    Send request to File Management microservice to get user stories from xslx file.

    request:
        xsls file

    response:
        json list of user stories find in input file like
        {
            "status": "success",
            "stories": [
                "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
                "As a transportation planner, I want to use inverse reinforcement learning to understand the underlying motivations and decision-making processes of drivers, so that I can improve traffic management and reduce accidents."
            ]
        }
    """
    file = request.files['stories']
    files = {'stories': (file.filename, file.stream, file.mimetype)}
    response = requests.post(f"{MICROSERVICES['file_management']}/storiesload", files=files)
    return jsonify(response.json()), response.status_code

@app.route('/predict/domain', methods=['POST'])
def predict_domain():
    """
    Send request to Predict Domain microservice to get domain from a single user story.

    request:
        json like
        {
            "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
        }

    response:
        json like
        {
            "domain": "Cardiology",
            "status": "success"
        }
    """
    data = request.get_json()
    response = requests.post(f"{MICROSERVICES['domain_prediction']}/predict/domain", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/predict/tasks', methods=['POST'])
def predict_tasks():
    """
    Send request to Predict Task microservice to get tasks from user story and its domain.

    request:
        json like
        {
            "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
            "domain": "Cardiology"
        }

    response:
        json like
        {
            "status": "success",
            "tasks": ["classification", "ranking"],
            "tasks_features": {
                "classification": ["race", "age", "sex"],
                "ranking": ["race", "age", "sex"]
            }
        }
    """
    data = request.get_json()
    response = requests.post(f"{MICROSERVICES['task_prediction']}/predict/tasks", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/generate/report', methods=['POST'])
def generate_report():
    """
    Send request to Generate Report microservice to get domain and tasks from multiple user stories.

    response:
        {
            "user_stories": [
                "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
                "As a transportation planner, I want to use inverse reinforcement learning to understand the underlying motivations and decision-making processes of drivers, so that I can improve traffic management and reduce accidents."
            ]
        }

    response:
        [
            {
                "user_story": "As a cardiologist, I want to identify multiword expressions in patient notes to identify risk factors for heart disease.",
                "domain": "Cardiology",
                "tasks": ["classification", "ranking"],
                "tasks_features": {
                    "classification": ["race", "age", "sex"],
                    "ranking": ["race", "age", "sex"]
                }
            },
            {
                "user_story": "As a transportation planner, I want to use inverse reinforcement learning to understand the underlying motivations and decision-making processes of drivers, so that I can improve traffic management and reduce accidents.",
                "domain": "Transportation",
                "tasks": ["pricing"],
                "tasks_features": {
                    "pricing": ["geography"]
                }
            }
        ]
    """
    data = request.get_json()
    response = requests.post(f"{MICROSERVICES['report_generation']}/generate/report", json=data)
    return response.content, response.status_code, {"Content-Type": "application/json"}

@app.route('/feedback/domain', methods=['POST'])
def feedback_domain():
    """
    Send request to Feedback microservice to store feedback user for a prediction domain result and retrain modal of domain predict.

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
    response = requests.post(f"{MICROSERVICES['feedback']}/feedback/domain", json=data)
    return response.content, response.status_code, {"Content-Type": "application/json"}

@app.route('/feedback/tasks', methods=['POST'])
def feedback_tasks():
    """
    Send request to Feedback microservice to store feedback user for a prediction tasks result and retrain modal of tasks predict.

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
    response = requests.post(f"{MICROSERVICES['feedback']}/feedback/tasks", json=data)
    return response.content, response.status_code, {"Content-Type": "application/json"}

if __name__ == '__main__':
    app.run(port=8080)
