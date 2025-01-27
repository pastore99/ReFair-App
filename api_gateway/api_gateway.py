from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# URL dei microservizi
MICROSERVICES = {
    "file_management": "http://localhost:5001",
    "domain_prediction": "http://localhost:5002",
    "task_prediction": "http://localhost:5003",
    "report_generation": "http://localhost:5004"
}

@app.route('/storiesload', methods=['POST'])
def stories_load():
    """Inoltra la richiesta al microservizio File Management."""
    file = request.files['stories']
    files = {'stories': (file.filename, file.stream, file.mimetype)}
    response = requests.post(f"{MICROSERVICES['file_management']}/storiesload", files=files)
    return jsonify(response.json()), response.status_code

@app.route('/predict/domain', methods=['POST'])
def predict_domain():
    """Inoltra la richiesta al microservizio Domain Prediction."""
    data = request.get_json()
    response = requests.post(f"{MICROSERVICES['domain_prediction']}/predict/domain", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/predict/tasks', methods=['POST'])
def predict_tasks():
    """Inoltra la richiesta al microservizio Task Prediction."""
    data = request.get_json()
    response = requests.post(f"{MICROSERVICES['task_prediction']}/predict/tasks", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/generate/report', methods=['POST'])
def generate_report():
    """Inoltra la richiesta al microservizio Report Generation."""
    data = request.get_json()
    response = requests.post(f"{MICROSERVICES['report_generation']}/generate/report", json=data)
    return response.content, response.status_code, {"Content-Type": "application/json"}

if __name__ == '__main__':
    app.run(port=8080)
