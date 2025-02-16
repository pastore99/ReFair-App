import json

class TestDesktop:
    def test_desktop_download_all(self, desktop_download_all_fixture):
        """
        Compares the contents of two JSON files containing all the data: one from a desktop application and the other from an Oracle.
        If the contents differ, an assertion error will be raised.
        """
        desktop_app_results = desktop_download_all_fixture[0]
        oracle = desktop_download_all_fixture[1]

        try:
            with open(desktop_app_results, 'r') as f1:
                data1 = json.load(f1)
        except json.JSONDecodeError as e:
            assert False, f"Error decoding JSON from {desktop_app_results}: {str(e)}"

        try:
            with open(oracle, 'r') as f2:
                data2 = json.load(f2)
        except json.JSONDecodeError as e:
            assert False, f"Error decoding JSON from {oracle}: {str(e)}"

        assert data1 == data2, f"The content of {desktop_app_results} and {oracle} is not equal."

    def test_desktop_single_us(self, desktop_single_us_fixture):
        """
        Compares the contents of two JSON files containing a single US: one from a desktop application and the other from an Oracle.
        If the contents differ, an assertion error will be raised.
        """
        desktop_app_results = desktop_single_us_fixture[0]
        oracle = desktop_single_us_fixture[1]

        try:
            with open(desktop_app_results, 'r') as f1:
                data1 = json.load(f1)
        except json.JSONDecodeError as e:
            assert False, f"Error decoding JSON from {desktop_app_results}: {str(e)}"

        try:
            with open(oracle, 'r') as f2:
                data2 = json.load(f2)
        except json.JSONDecodeError as e:
            assert False, f"Error decoding JSON from {oracle}: {str(e)}"

        assert data1 == data2, f"The content of {desktop_app_results} and {oracle} is not equal."
