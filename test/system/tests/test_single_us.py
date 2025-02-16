import json
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATTERN = r'^(?!\s*$).{1,1024}$'

class Test_single_us:

    def test_single_us_tc_1(self, driver):
        """
        Insert a user story that does not match the expected regex pattern.
        Verifies that an alert with the message
        'The User Story did not match the required format.' is displayed.
        """

        expected_alert_message = "The User Story did not match the required format."

        driver.get('http://localhost:5173/')

        user_Story = ""  # Caso di input non valido

        # Inserisce la user story vuota nell'input
        driver.find_element(By.CSS_SELECTOR, ".entry_area").find_element(By.TAG_NAME, "input").send_keys(user_Story)
        driver.find_element(By.CSS_SELECTOR, ".analyze").click()

        try:
            # Attende l'alert e lo cattura
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text

            print(f"Alert detected: {alert_text}")  # Debug per verificare il messaggio
            assert alert_text == expected_alert_message, f"Unexpected alert text: {alert_text}"

            alert.accept()  # Chiude l'alert cliccando su "OK"

        except TimeoutException:
            assert False, f"Alert with the message '{expected_alert_message}' did not appear."

        except NoAlertPresentException:
            assert False, "No alert was found, but one was expected."

    def test_single_us_tc_2(self, driver, analyze_tc_1_fixture):
        """
        Insert a user story that matches the expected pattern in the input text area and analyze it.
        Verifies if the result is equal to the oracle.
        """

        driver.get('http://localhost:5173/')

        oracle_path = analyze_tc_1_fixture[1]
        user_Story = (
            "As a librarian, I want to use artificial neural networks to analyze user behavior and improve library services, so that we can provide a better experience for our patrons."
        )

        # Inserisce la user story valida nell'input e clicca su analyze
        driver.find_element(By.CSS_SELECTOR, ".entry_area").find_element(By.TAG_NAME, "input").send_keys(user_Story)
        driver.find_element(By.CSS_SELECTOR, ".analyze").click()

        try:
            # Attende che siano presenti gli elementi con classe '.mx-4'
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".mx-4"))
            )
            if len(elements) < 2:
                raise NoSuchElementException(f"Expected at least 2 elements with class 'mx-4', got {len(elements)}")

            # Attende che il testo del secondo elemento sia non vuoto
            domain_text = WebDriverWait(driver, 10).until(
                lambda d: elements[1].text.strip() if elements[1].text.strip() != "" else False
            )

            if ': ' not in domain_text:
                raise ValueError(f"Unexpected format for domain text: {domain_text}")
            domain = domain_text.split(': ', 1)[1].strip()

            # Attende la presenza delle righe della tabella (ogni riga è un <tr> all'interno del <tbody>)
            table_rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '/html/body/div/div/div[3]/div/div/div[2]/div[1]/table/tbody/tr'))
            )
            features = {}
            for row in table_rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if len(cells) < 2:
                    raise NoSuchElementException("Expected at least 2 cells in a table row, found less.")
                key = cells[0].text.strip()
                # Supponiamo che il contenuto della seconda cella sia nel formato 'val1 - val2'
                value = [v.strip() for v in cells[1].text.split(' - ')]
                features[key] = value

            # Legge i dati dell'oracolo
            # Legge i dati dell'oracolo
            with open(oracle_path, 'r') as file:
                oracle_data = json.load(file)

            # Se oracle_data è una lista, prendi il primo elemento
            if isinstance(oracle_data, list):
                oracle_data = oracle_data[0]

            # Ora puoi accedere a 'domain' e 'features'
            assert domain == oracle_data['domain'], f"Domain does not match the oracle. Found: {domain}, expected: {oracle_data['domain']}"
            assert features == oracle_data['tasks_features'], f"Sensitive features do not match the oracle. Found: {features}, expected: {oracle_data['features']}"

        except TimeoutException:
            assert False, "Modal did not appear."
        except NoSuchElementException as e:
            assert False, f"No matching with the oracle: {str(e)}"
        except Exception as e:
            assert False, str(e)
