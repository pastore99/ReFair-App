import json

class ReportGenerator:
    def __init__(self, prediction_service):
        self.prediction_service = prediction_service

    def generate(self, user_stories):
        """
        Generate report from list of user story

        :param user_stories: list of user story
        :return: domain end tasks predictions
        """
        analyzed_stories = []

        for story in user_stories:
            try:
                domain = self.prediction_service.get_domain(story)
                tasks, tasks_features = self.prediction_service.get_tasks(story, domain)

                analyzed_stories.append({
                    "user_story": story,
                    "domain": domain,
                    "tasks": tasks,
                    "tasks_features": tasks_features
                })
            except ValueError as e:
                analyzed_stories.append({
                    "user_story": story,
                    "status": "failure",
                    "motivation": str(e)
                })

        return json.dumps(analyzed_stories, indent=4)
