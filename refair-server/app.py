from flask import Flask, Response, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS


from REFAIR import get_domain
from REFAIR import get_ml_task
from REFAIR import feature_extraction

import pandas as pd
import json

ALLOWED_EXTENSIONS = {'xlsx'}


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/storiesload', methods=['POST'])
def load_stories():
    """
    Loads the user stories from an uploaded Excel file and checks for the 'User Story' column.
    
    Keyword arguments:
    None (file provided via POST request)
    
    Return: JSON response with status 'success' and loaded stories or 'failure' with error message
    """

    if request.method == 'POST':
        # check if the post request has the file part
        if 'stories' not in request.files:
            return jsonify({
                'status': 'failure',
                'motivation': "No file \"stories.xlsx\" loaded"
            })
        
        file = request.files['stories']
        
        if not allowed_file(file.filename):
            return jsonify({
                'status': 'failure',
                'motivation': "No file \"stories.xlsx\" loaded"
            })


        stories = pd.read_excel(file)

        if 'User Story' in stories:
            return jsonify({
                'status': 'success',
                'stories': stories["User Story"].tolist()
            })
        else:  return jsonify({
                'status': 'failure',
                'motivation': "No column \"User Story\" found"
            })


@app.route('/analyzeStory', methods = ['POST','GET'])
def analysis():
    """
    Analyzes a single user story, predicts its domain, associated machine learning tasks, 
    and sensitive features, then returns the results as a JSON response.
    
    Keyword arguments:
    None (story provided via POST request form)
    
    Return: JSON response with domain, tasks, task features, and number of unique features
    """
    
    if request.method == 'POST':
        story = request.form['story']  
        domain = get_domain(story)
        ml_tasks = get_ml_task(story, domain)

        tasks_features = feature_extraction(domain, ml_tasks)

        unique_features = {}
        for features in tasks_features.values():
            for feature in features:
                if feature in unique_features:
                    unique_features[feature] = unique_features[feature] + 1 
                else:
                     unique_features[feature] = 1


        return jsonify(
            domain=domain,
            tasks=ml_tasks,
            tasks_features=tasks_features,
            features_counts = unique_features
        )
    else: return "Not Allowed"
    


@app.route('/reportStories', methods = ['POST','GET'])
def reportStories():
    """
    Analyzes multiple user stories, predicts the domain, tasks, and features for each, 
    then returns the results as a downloadable JSON file.
    
    Keyword arguments:
    None (stories provided via POST request form in JSON format)
    
    Return: JSON file with analyzed stories data
    """
    
    if request.method == 'POST':
        analyzed_stories = []

        stories = json.loads(request.form['stories']) 

        
        for story in stories:
            domain = get_domain(story)
            ml_tasks = get_ml_task(story, domain)

            features = feature_extraction(domain, ml_tasks)

            analyzed_stories.append({"story": story, "domain":domain, "tasks":ml_tasks,"features":features})

        content = str(analyzed_stories)
        return Response(content, 
                mimetype='application/json',
                headers={'Content-Disposition':'attachment;filename=zones.geojson'})

        
    else: return "Not Allowed"


@app.route('/reportStory', methods = ['POST','GET'])
def reportStory():
    """
    Analyzes a single user story, predicts its domain, tasks, and features, 
    then returns the result as a downloadable JSON file.
    
    Keyword arguments:
    None (story provided via POST request form in JSON format)
    
    Return: JSON file with the analyzed story data
    """
    
    if request.method == 'POST':
        analyzed_stories = []

        story = json.loads(request.form['story']) 

        
        domain = get_domain(story)
        ml_tasks = get_ml_task(story, domain)

        features = feature_extraction(domain, ml_tasks)

        analyzed_story = {"story": story, "domain":domain, "tasks":ml_tasks,"features":features}

        content = str(analyzed_story)
        return Response(content, 
                mimetype='application/json',
                headers={'Content-Disposition':'attachment;filename=zones.geojson'})

        
    else: return "Not Allowed"



def allowed_file(filename):
    """
    Checks if the uploaded file is an allowed file type based on its extension.
    
    Keyword arguments:
    filename -- the name of the uploaded file (string)
    
    Return: True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)