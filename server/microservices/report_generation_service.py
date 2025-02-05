from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from services.prediction_service import PredictionService
from services.report_generator import ReportGenerator

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# Configurazione URL microservizi
DOMAIN_SERVICE_URL = "http://localhost:5002/predict/domain"
TASK_SERVICE_URL = "http://localhost:5003/predict/tasks"

# Dependency Injection
prediction_service = PredictionService(DOMAIN_SERVICE_URL, TASK_SERVICE_URL)
report_generator = ReportGenerator(prediction_service)

@app.route('/generate/report', methods=['POST'])
def generate_report():
    """
    Get domain and tasks from multiple user stories.

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
    if not request.is_json:
        return jsonify({"status": "failure", "motivation": "Request body must be JSON"})

    data = request.get_json()
    user_stories = data.get('user_stories')

    if not user_stories or not isinstance(user_stories, list):
        return jsonify({"status": "failure", "motivation": "Missing 'user_stories' (list) in request"})

    try:
        report_content = report_generator.generate(user_stories)
        return Response(
            report_content,
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=report.json'}
        )
    except Exception as e:
        return jsonify({"status": "failure", "motivation": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5004)
