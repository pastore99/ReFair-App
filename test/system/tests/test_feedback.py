import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestFeedbackSystem:

    @pytest.fixture
    def driver(self, driver_with_options):
        """ Restituisce il WebDriver configurato """
        return driver_with_options

    def test_feedback_tc_1(self, driver, load_tc_5_fixture):
        """
        Feedback_TC_1: VD1, VT1 (Success)
        Scenario: Voto dominio (VD) e voto task (VT) entrambi validi (1-5).
        Esito atteso: Successo.
        """
        driver.get("http://localhost:5173/")

        # Caricare il file
        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_5_fixture)
        driver.find_element(By.CSS_SELECTOR, ".load").click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))

        # Cliccare "Analyze"
        analyze_button = driver.find_element(By.CSS_SELECTOR, "table tbody tr:first-child .analyze")
        analyze_button.click()

        # Aprire finestra valutazione
        rate_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.rating")))
        rate_button.click()

        # Selezionare voti validi
        stars_domain = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rating-section:nth-of-type(1) .rating-container span")))
        stars_domain[3].click()  # 4 stelle dominio

        stars_task = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rating-section:nth-of-type(2) .rating-container span")))
        stars_task[4].click()  # 5 stelle task

        # Inviare valutazione
        submit_button = driver.find_element(By.CSS_SELECTOR, ".button.submit-rating")
        submit_button.click()

        # Verifica successo
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        assert "Rating submitted successfully!" in alert.text
        alert.accept()

    def test_feedback_tc_2(self, driver, load_tc_5_fixture):
        """
        Feedback_TC_2: VD1, VT2 (Error)
        Scenario: Voto dominio (VD) valido, ma voto task (VT) mancante.
        Esito atteso: Errore.
        """
        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_5_fixture)
        driver.find_element(By.CSS_SELECTOR, ".load").click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))

        analyze_button = driver.find_element(By.CSS_SELECTOR, "table tbody tr:first-child .analyze")
        analyze_button.click()

        rate_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.rating")))
        rate_button.click()

        # Selezionare solo voto dominio
        stars_domain = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rating-section:nth-of-type(1) .rating-container span")))
        stars_domain[3].click()

        submit_button = driver.find_element(By.CSS_SELECTOR, ".button.submit-rating")
        submit_button.click()

        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        assert "Please select a rating for both domain and task identification." in alert.text
        alert.accept()

    def test_feedback_tc_3(self, driver, load_tc_5_fixture):
        """
        Feedback_TC_3: VD2, VT2 (Error)
        Scenario: Nessun voto selezionato (VD e VT mancanti).
        Esito atteso: Errore.
        """
        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_5_fixture)
        driver.find_element(By.CSS_SELECTOR, ".load").click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))

        analyze_button = driver.find_element(By.CSS_SELECTOR, "table tbody tr:first-child .analyze")
        analyze_button.click()

        rate_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.rating")))
        rate_button.click()

        submit_button = driver.find_element(By.CSS_SELECTOR, ".button.submit-rating")
        submit_button.click()

        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        assert "Please select a rating for both domain and task identification." in alert.text
        alert.accept()

    def test_feedback_tc_4(self, driver, load_tc_5_fixture):
        """
        Feedback_TC_4: VD2, VT1 (Error)
        Scenario: Nessun voto dominio (VD), ma voto task (VT) valido.
        Esito atteso: Errore.
        """
        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_5_fixture)
        driver.find_element(By.CSS_SELECTOR, ".load").click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))

        analyze_button = driver.find_element(By.CSS_SELECTOR, "table tbody tr:first-child .analyze")
        analyze_button.click()

        rate_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.rating")))
        rate_button.click()

        # Selezionare solo voto task
        stars_task = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rating-section:nth-of-type(2) .rating-container span")))
        stars_task[2].click()  # 3 stelle task

        submit_button = driver.find_element(By.CSS_SELECTOR, ".button.submit-rating")
        submit_button.click()

        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        assert "Please select a rating for both domain and task identification." in alert.text
        alert.accept()
