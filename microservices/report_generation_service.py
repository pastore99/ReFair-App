from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import requests
import json

# Configurazione Flask
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# Endpoint degli altri microservizi
DOMAIN_SERVICE_URL = "http://localhost:5002/predict/domain"
TASK_SERVICE_URL = "http://localhost:5003/predict/tasks"

@app.route('/generate/report', methods=['POST'])
def generate_report():
    """
    Genera un report per una o più user stories, chiamando i microservizi di predizione del dominio e dei task.
    """
    if not request.is_json:
        return jsonify({
            "status": "failure",
            "motivation": "Request body must be JSON"
        })

    # Estrarre le user stories dal corpo della richiesta
    data = request.get_json()
    user_stories = data.get('user_stories')

    if not user_stories or not isinstance(user_stories, list):
        return jsonify({
            "status": "failure",
            "motivation": "Missing 'user_stories' (list) in request"
        })

    analyzed_stories = []

    for story in user_stories:
        # Step 1: Predizione del dominio
        domain_response = requests.post(DOMAIN_SERVICE_URL, json={"user_story": story})
        if domain_response.status_code != 200 or domain_response.json().get("status") != "success":
            return jsonify({
                "status": "failure",
                "motivation": f"Failed to predict domain for story: {story}"
            })
        domain = domain_response.json().get("domain")

        # Step 2: Predizione dei task e delle feature
        task_response = requests.post(TASK_SERVICE_URL, json={"user_story": story, "domain": domain})
        if task_response.status_code != 200 or task_response.json().get("status") != "success":
            return jsonify({
                "status": "failure",
                "motivation": f"Failed to predict tasks for story: {story}"
            })
        tasks = task_response.json().get("tasks")
        tasks_features = task_response.json().get("tasks_features")

        # Step 3: Creazione del risultato per la storia
        analyzed_stories.append({
            "user_story": story,
            "domain": domain,
            "tasks": tasks,
            "tasks_features": tasks_features
        })

    # Creazione del file JSON come risultato
    report_content = json.dumps(analyzed_stories, indent=4)
    return Response(
        report_content,
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment;filename=report.json'}
    )

if __name__ == '__main__':
    app.run(port=5004)
