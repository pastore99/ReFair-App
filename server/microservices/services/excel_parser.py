import pandas as pd
import re

PATTERN = r'^(?!\s*$).{1,1024}$'

class ExcelParser:
    @staticmethod
    def parse_stories(file_path):
        try:
            stories_df = pd.read_excel(file_path, engine="openpyxl")

            if 'User Story' not in stories_df.columns:
                raise ValueError("No column 'User Story' found in the file")

            user_stories = stories_df["User Story"].dropna().tolist()

            if not all(isinstance(story, str) for story in user_stories):
                raise ValueError("The file could not be loaded because at least one non-textual element was found in the 'User Story' column.")

            if len(user_stories) == 0:
                raise ValueError("There are no user stories")

            valid_stories = [story for story in user_stories if re.fullmatch(PATTERN, story)]
            warning_message = None

            if len(valid_stories) < len(user_stories):
                warning_message = "The file was loaded successfully, but some user stories did not match the required format and were not included."

            return {
                "stories": valid_stories,
                "warning": warning_message  # Aggiungiamo il messaggio di avviso nella risposta
            }

        except Exception as e:
            return {"error": str(e)}  # Ritorniamo un errore JSON leggibile
