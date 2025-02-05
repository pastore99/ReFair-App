from flask import Flask, jsonify, request
from flask_cors import CORS
from services.classifier_factory import  ClassifierFactory

# Configurazione Flask
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# Otteniamo il classificatore corretto dalla Factory
domain_classifier = ClassifierFactory.get_domain_classifier()

@app.route('/predict/domain', methods=['POST'])
def predict_domain():
    """
    Get domain from a single user story.

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
    if not request.is_json:
        return jsonify({
            "status": "failure",
            "motivation": "Request body must be JSON"
        }), 400

    # Estrae la user story dal corpo della richiesta
    data = request.get_json()
    user_story = data.get('user_story')

    if not user_story:
        return jsonify({
            "status": "failure",
            "motivation": "Missing 'user_story' in request"
        }), 400

    # Predizione
    try:
        domain = domain_classifier.predict(user_story)
        return jsonify({
            "status": "success",
            "domain": domain
        })
    except Exception as e:
        return jsonify({
            "status": "failure",
            "motivation": f"Prediction error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(port=5002)