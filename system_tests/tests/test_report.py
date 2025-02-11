import json
import os.path
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class TestReport:

    @pytest.mark.parametrize('driver_with_options', ['report_single_us_tc_1'], indirect=True)
    def test_report_single_us_tc_1(self, driver_with_options, analyze_tc_1_fixture):
        """
        Upload a well-formed Excel file and check if the single file .json downloaded is equal to the oracle
        """

        driver_with_options.get('http://localhost:5173/')

        excel, oracle = analyze_tc_1_fixture

        file_input = driver_with_options.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(excel)

        driver_with_options.find_element(By.CSS_SELECTOR, ".load").click()

        try:
            WebDriverWait(driver_with_options, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div/div[1]/table/tbody/tr[1]/td[2]/div/button"))).click()
            time.sleep(2)
            WebDriverWait(driver_with_options, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div/div/div[3]/button"))).click()

            dowloaded_file = os.listdir(
                os.path.join(
                    os.path.dirname(__file__),
                    '..', 'data', 'report_single_us_tc_1'
                )
            )

            with open(oracle, 'r') as file, open(os.path.join(os.path.dirname(__file__), '..', 'data', 'report_single_us_tc_1', dowloaded_file[0]), 'r') as file1:
                oracle_data = json.load(file)
                report = json.load(file1)

                report["story"] = report["story"].replace("\n", "")

                assert report == oracle_data, "the report does not match the oracle data"

        except TimeoutException:
            assert False, "Modal did not appear."
        except NoSuchElementException:
            assert False, "No element was found in the page."


    @pytest.mark.parametrize('driver_with_options', ['report_tc_1'], indirect=True)
    def test_report_tc_1(self, driver_with_options, analyze_tc_1_fixture):
        """
        Upload a well-formed Excel file and check if the downloaded file .json is equal to the oracle
        """

        driver_with_options.get('http://localhost:5173/')

        excel = analyze_tc_1_fixture[0]

        file_input = driver_with_options.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(excel)

        driver_with_options.find_element(By.CSS_SELECTOR, ".load").click()

        try:
            WebDriverWait(driver_with_options, 15).until(EC.element_to_be_clickable((By.ID, "report"))).click()

            time.sleep(20)

            dowloaded_file = os.path.join(
                os.path.dirname(__file__),
                '..', 'data', 'report_tc_1', 'report.json'
            )

            oracle = os.path.join(
                    os.path.dirname(__file__),
                    '..', 'data', 'report_tc_1', 'oracle.json'
                )

            with open(oracle, 'r') as file, open(dowloaded_file, 'r') as file1:
                oracle_data = json.load(file)
                report = json.load(file1)

                # Rimuove i newline alla fine delle user_story in entrambi i file
                for item in report:
                    item["user_story"] = item["user_story"].strip()

                for item in oracle_data:
                    item["user_story"] = item["user_story"].strip()

                assert report == oracle_data, "the report does not match the oracle data"

        except TimeoutException:
            assert False, "Modal did not appear."
        except NoSuchElementException:
            assert False, "No element was found in the page."


    @pytest.mark.parametrize('driver_with_options', ['report_tc_2'], indirect=True)
    def test_report_tc_2(self, driver_with_options, report_tc_2):
        """
        Upload a well-formed Excel file and check if all the downloaded file .json are equal to the oracle
        """

        driver_with_options.get('http://localhost:5173/')

        excel = report_tc_2[0]

        file_input = driver_with_options.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(excel)

        driver_with_options.find_element(By.CSS_SELECTOR, ".load").click()

        try:
            WebDriverWait(driver_with_options, 15).until(EC.element_to_be_clickable((By.ID, "report"))).click()

            time.sleep(30)

            dowloaded_file = os.path.join(
                    os.path.dirname(__file__),
                    '..', 'data', 'report_tc_2', 'report.json'
                )

            oracle = os.path.join(
                    os.path.dirname(__file__),
                    '..', 'data', 'report_tc_2', 'oracle.json'
                )

            with open(oracle, 'r') as file, open(dowloaded_file, 'r') as file1:
                oracle_data = json.load(file)
                report = json.load(file1)

                assert report == oracle_data, "the report does not match the oracle data"

        except TimeoutException:
            assert False, "Modal did not appear."
        except NoSuchElementException:
            assert False, "No element was found in the page."


    def test_report_tc3(self, driver):
        """
        Check if the report button is disabled with no file loaded
        """

        driver.get('http://localhost:5173/')

        try:
            assert driver.find_element(By.ID, "report").is_enabled() is False, "The report button is not disabled"

        except NoSuchElementException:
            assert False, "No element was found in the page."




