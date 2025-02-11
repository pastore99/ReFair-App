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
            # Attende la presenza di un elemento con classe 'alert' contenente il messaggio atteso
            alert_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".alert"))
            )
            assert alert_element.text == expected_alert_message, f"Unexpected alert text: {alert_element.text}"
        except TimeoutException:
            assert False, f"Alert with the message '{expected_alert_message}' did not appear."

    def test_single_us_tc_2(self, driver, analyze_tc_1_fixture):
        """
        Insert a user story that matches the expected pattern in the input text area and analyze it.
        Verifies if the result is equal to the oracle.
        """

        driver.get('http://localhost:5173/')

        oracle_path = analyze_tc_1_fixture[1]
        user_Story = (
            "As a dedicated and passionate computer vision researcher working in the rapidly evolving field of artificial intelligence, I am deeply committed to advancing the capabilities of machine learning techniques. My primary objective is to utilize sophisticated and cutting-edge machine learning models to analyze large volumes of video and image data, extracting valuable insights and identifying subtle, complex patterns that may be extremely challenging, or even impossible, for human observers to discern with the naked eye. By employing a diverse range of deep learning architectures, such as convolutional neural networks (CNNs), recurrent neural networks (RNNs), and transformer-based models, I aim to enhance the precision and robustness of computer vision systems. These systems are intended to excel in a variety of applications, including but not limited to, object detection, facial recognition, medical imaging, autonomous vehicle navigation, and intelligent surveillance. Through this meticulous process of pattern recognition and data analysis, I seek to uncover hidden correlations and anomalies within the data that can lead to significant breakthroughs in the understanding and interpretation of visual information. My goal is to not only improve the accuracy and reliability of existing computer vision algorithms but also to contribute to the development of innovative applications that push the boundaries of what is possible in this domain. Ultimately, by advancing the state of the art in machine learning-driven computer vision, I hope to contribute meaningfully to the creation of more intelligent, adaptive, and responsive systems. These systems should be capable of performing complex visual tasks with a high degree of autonomy and precision, thereby enabling new possibilities for technological advancement and societal benefit across multiple sectors."
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
            with open(oracle_path, 'r') as file:
                oracle_data = json.load(file)

            assert domain == oracle_data['domain'], f"Domain does not match the oracle. Found: {domain}, expected: {oracle_data['domain']}"
            assert features == oracle_data['features'], f"Sensitive features do not match the oracle. Found: {features}, expected: {oracle_data['features']}"

        except TimeoutException:
            assert False, "Modal did not appear."
        except NoSuchElementException as e:
            assert False, f"No matching with the oracle: {str(e)}"
        except Exception as e:
            assert False, str(e)
