import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class TestAnalyze:

    def test_analyze_tc_1(self, driver, analyze_tc_1_fixture):
        """
        Upload a well-formed Excel file and check whether the domain and sensitive characteristics
        of the USs provided are the same as those of the oracle file.
        """

        driver.get('http://localhost:5173/')

        excel, oracle = analyze_tc_1_fixture

        # 🛠 Attendere che la pagina sia completamente caricata
        time.sleep(10)  # Attesa fissa per garantire che il JS sia eseguito (da rimuovere se inutile)

        # Caricamento del file Excel
        try:
            file_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".form-control"))
            )
            file_input.send_keys(excel)
        except TimeoutException:
            print("\n🔴 ERRORE: Il campo di input del file non è stato trovato.")
            print(driver.page_source)  # Stampiamo il codice HTML attuale per debug
            assert False, "File input not found."

        # Cliccare sul pulsante di caricamento
        try:
            load_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".load"))
            )
            load_button.click()
        except TimeoutException:
            print("\n🔴 ERRORE: Il pulsante di caricamento non è stato trovato.")
            print(driver.page_source)  # Stampiamo il codice HTML attuale per debug
            assert False, "Load button not found."

        try:
            # 🛠 Attende il caricamento della tabella
            WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.XPATH, "//table/tbody"))
            )

            # 🛠 Verifica che il pulsante della modale esista prima di cliccarlo
            modal_button_xpath = "//table/tbody/tr[1]/td[2]/div/button"
            modal_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, modal_button_xpath))
            )

            modal_button.click()
        except TimeoutException:
            print("\n🔴 ERRORE: Il pulsante della modale non è stato trovato.")
            print(driver.page_source)  # Stampiamo il codice HTML attuale per debug
            assert False, "Modal button not found."

        # 🛠 Attende che gli elementi con classe `.mx-4` siano visibili e non vuoti
        try:
            WebDriverWait(driver, 25).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, ".mx-4")) > 1
            )
            WebDriverWait(driver, 25).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, ".mx-4")[1].text.strip() != ""
            )
        except TimeoutException:
            print("\n🔴 ERRORE: La pagina non ha caricato i dati correttamente.")
            print(driver.page_source)  # Stampiamo il codice HTML attuale per debug
            assert False, "Data not loaded."

        # 🛠 Estrazione del dominio
        elements = driver.find_elements(By.CSS_SELECTOR, ".mx-4")
        domain_text = elements[1].text
        domain = domain_text.split(': ')[1] if ': ' in domain_text else domain_text

        # 🛠 Estrazione delle features dalla tabella
        table_body = driver.find_elements(By.XPATH, "//div[3]/div/div/div[2]/div[1]/table/tbody")
        features = {}
        if table_body:
            for row in table_body:
                cols = row.find_elements(By.TAG_NAME, 'td')
                if len(cols) >= 2:
                    features[cols[0].text] = cols[1].text.split(' - ')

        # 🛠 Confronto con l'oracolo
        with open(oracle, 'r') as file:
            oracle_data = json.load(file)

        assert domain == oracle_data['domain'], f"Domain does not match the oracle: expected '{oracle_data['domain']}', got '{domain}'"
        assert features == oracle_data['features'], "Sensitive features does not match the oracle"
