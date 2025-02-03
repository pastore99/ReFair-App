from flask import Flask
from flask_cors import CORS

# Importa le funzioni degli endpoint dai moduli di supporto
from feedback_utlis.domain_feedback import get_domain_feedback
from feedback_utlis.task_feedback import get_tasks_feedback

app = Flask(__name__)
CORS(app)

# Endpoint per il dominio
@app.route('/feedback/domain', methods=['POST'])
def feedback_domain():
    return get_domain_feedback()

# Endpoint per i task
@app.route('/feedback/tasks', methods=['POST'])
def feedback_tasks():
    return get_tasks_feedback()

if __name__ == '__main__':
    app.run(port=5005)
