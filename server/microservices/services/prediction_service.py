import requests

class PredictionService:
    def __init__(self, domain_service_url, task_service_url):
        self.domain_service_url = domain_service_url
        self.task_service_url = task_service_url

    def get_domain(self, user_story):
        """
        Send user stoy to Domain Predict microservice.

        :param user_story: user story to analyze
        :return: json of domain predict
        """
        response = requests.post(self.domain_service_url, json={"user_story": user_story})
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("domain")
        raise ValueError(f"Failed to predict domain for story: {user_story}")

    def get_tasks(self, user_story, domain):
        """
        Send user story and domain to Task Prediction Microservice.
        
        :param user_story: user story to analyze
        :param domain: domain of user story to analyze
        :return: the json result of prediction
        """""
        response = requests.post(self.task_service_url, json={"user_story": user_story, "domain": domain})
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("tasks"), data.get("tasks_features")
        raise ValueError(f"Failed to predict tasks for story: {user_story}")
