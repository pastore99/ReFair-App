import pandas as pd
import re

PATTERN = r'^(?!\s*$).{1,1024}$'

class ExcelParser:
    @staticmethod
    def parse_stories(file_path):
        """
        Read excel file and return 'User Story' column if it contains valid data.

        :param file_path: the path of excel file
        :return: list of user stories that match the pattern
        """
        try:
            stories_df = pd.read_excel(file_path, engine="openpyxl")

            if 'User Story' not in stories_df.columns:
                raise ValueError("No column 'User Story' found in the file")

            user_stories = stories_df["User Story"].dropna().tolist()

            # Check if all values in 'User Story' column are text
            if not all(isinstance(story, str) for story in user_stories):
                raise ValueError("The file could not be loaded because at least one non-textual element was found in the 'User Story' column.")

            if len(user_stories) == 0:
                raise ValueError("There are no user stories")

            # Filtra le user stories che rispettano il pattern
            valid_stories = [story for story in user_stories if re.fullmatch(PATTERN, story)]

            if len(valid_stories) < len(user_stories):
                print("Some user stories did not match the required format and were not included.")

            return valid_stories

        except Exception as e:
            raise ValueError(f"Error reading Excel file: {str(e)}")
