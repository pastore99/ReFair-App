from flask import Flask, jsonify, request
from flask_cors import CORS
from services.file_service import FileService
from services.excel_parser import ExcelParser

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

UPLOAD_FOLDER = "uploads"
file_service = FileService(UPLOAD_FOLDER)

@app.route('/storiesload', methods=['POST'])
def load_stories():
    """
    Get user stories from xslx file.

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
    if 'stories' not in request.files:
        return jsonify({"status": "failure", "motivation": "No file 'stories.xlsx' uploaded"})
    file = request.files['stories']
    try:
        file_path = file_service.save_file(file, file.filename)
        stories = ExcelParser.parse_stories(file_path)
        return jsonify({"status": "success", "stories": stories})
    except ValueError as e:
        return jsonify({"status": "failure", "motivation": str(e)})
    except Exception as e:
        return jsonify({"status": "failure", "motivation": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5001)