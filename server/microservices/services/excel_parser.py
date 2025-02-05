import pandas as pd

class ExcelParser:
    @staticmethod
    def parse_stories(file_path):
        """
        Read excel file and return 'user story' column

        :param file_path: the path of excel file
        :return: json with all user stories that it found
        """
        try:
            stories_df = pd.read_excel(file_path)

            if 'User Story' not in stories_df.columns:
                raise ValueError("No column 'User Story' found in the file")

            return stories_df["User Story"].dropna().tolist()

        except Exception as e:
            raise ValueError(f"Error reading Excel file: {str(e)}")
