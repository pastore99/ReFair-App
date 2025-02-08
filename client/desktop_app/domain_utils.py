from http.client import responses
import requests

def getDomain(user_story):
    try:
        # Invia la richiesta con il JSON corretto
        response = requests.post('http://localhost:8080/predict/domain', json={"user_story": user_story})

        # Controlla lo stato della risposta
        if response.status_code == 200:
            data = response.json()
            if "domain" in data:
                return data["domain"]
            else:
                return "No domain found in response"
        else:
            return f"Server responded with {response.status_code}: {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"

def getMLTask(user_story, domain):
    data = {
        "user_story": user_story,
        "domain": domain
    }
    try:
        response = requests.post('http://localhost:8080/predict/tasks', json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Server respond with: {response.status_code}"

    except Exception as e:
        return f"An error occured: {e}"
