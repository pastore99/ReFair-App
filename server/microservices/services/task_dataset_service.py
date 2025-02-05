import os
import pandas as pd

class TaskDatasetService:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        domain_task_path = os.path.join(base_dir, '..', '..', 'utils', 'datasets', 'domains-tasks-mapping.csv')
        domains_mapping_path = os.path.join(base_dir, '..', '..', 'utils', 'datasets', 'domains-features-mapping.csv')
        tasks_mapping_path = os.path.join(base_dir, '..', '..', 'utils', 'datasets', 'tasks-features-mapping.csv')

        if not os.path.exists(domain_task_path) or not os.path.exists(domains_mapping_path) or not os.path.exists(tasks_mapping_path):
            raise FileNotFoundError("One or more dataset files are missing")

        self.domain_task_mapping = pd.read_csv(domain_task_path)
        self.domains_mapping = pd.read_csv(domains_mapping_path)
        self.tasks_mapping = pd.read_csv(tasks_mapping_path)

    def get_tasks_for_domain(self, domain, predicted_tasks):
        if not isinstance(domain, str):
            raise TypeError(f"Expected domain as str, got {type(domain)}")
        output = []
        for task in predicted_tasks:
            if not isinstance(task, str):
                raise TypeError(f"Expected task as str, got {type(task)}")

            filtered_df = self.domain_task_mapping[
                (self.domain_task_mapping['Domain'].astype(str).str.lower() == domain.lower()) &
                (self.domain_task_mapping['Task'].astype(str).str.lower() == task.lower())
                ]
            if not filtered_df.empty:
                output.append(task)

        return output

    def extract_features(self, domain, tasks):
        if not isinstance(domain, str):
            raise TypeError(f"Expected domain as str, got {type(domain)}")
        domain_features = self.domains_mapping[self.domains_mapping['Domain'].astype(str).str.lower() == domain.lower()]['Feature'].tolist()
        features_by_task = {}
        for task in tasks:
            if not isinstance(task, str):
                raise TypeError(f"Expected task as str, got {type(task)}")

            task_features = self.tasks_mapping[self.tasks_mapping['Task'].astype(str).str.lower() == task.lower()]['Feature'].tolist()
            features_by_task[task] = list(set(task_features) & set(domain_features))
        return features_by_task