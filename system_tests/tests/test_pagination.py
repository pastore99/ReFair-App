import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException

class TestPagination:

    def test_pagination(self, driver, load_tc_28_fixture):
        """
        Verifica che il primo e l'ultimo pulsante della paginazione siano disabilitati,
        rispettivamente sulla prima pagina e sull'ultima.
        """
        driver.get('http://localhost:5173/')

        try:
            # Attende che il campo di input sia presente e lo compila
            file_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".form-control"))
            )
            file_input.send_keys(load_tc_28_fixture)

            # Attende che il pulsante di caricamento sia cliccabile e lo clicca
            load_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".load"))
            )
            load_button.click()

            # Attende che l'elemento della paginazione sia presente
            pagination = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pagination"))
            )

            # Trova l'input numerico all'interno della paginazione e porta l'elemento in vista
            input_number = pagination.find_element(By.TAG_NAME, "input")
            driver.execute_script("arguments[0].scrollIntoView(true);", input_number)
            # Attende che l'input sia visibile ed abilitato
            WebDriverWait(driver, 35).until(lambda d: input_number.is_displayed() and input_number.is_enabled())

            # Recupera il valore massimo dal campo di input
            max_pagination = input_number.get_attribute("max")

            # Verifica che il primo pulsante della paginazione sia disabilitato sulla prima pagina
            first_button = pagination.find_elements(By.TAG_NAME, "button")[0]
            is_first_button_disabled = not first_button.is_enabled()

            # Per cambiare pagina si usa un click via JavaScript (più affidabile in caso di elementi parzialmente non interagibili)
            driver.execute_script("arguments[0].click();", input_number)
            input_number.send_keys(Keys.CONTROL + "a")
            input_number.send_keys(Keys.BACKSPACE)
            input_number.send_keys(max_pagination)
            input_number.send_keys(Keys.ENTER)

            # Attende che la nuova pagina venga caricata
            time.sleep(2)  # Valuta di sostituire con un'attesa esplicita basata su un indicatore specifico

            # Ricarica l'elemento paginazione per avere il DOM aggiornato
            pagination = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pagination"))
            )
            buttons = pagination.find_elements(By.TAG_NAME, "button")
            if len(buttons) < 2:
                raise NoSuchElementException("Numero insufficiente di pulsanti nella paginazione.")
            last_button = buttons[1]
            is_last_button_disabled = not last_button.is_enabled()

            # Verifica che entrambi i pulsanti siano disabilitati come previsto
            assert is_first_button_disabled and is_last_button_disabled, "Uno o entrambi i pulsanti non sono disabilitati"

        except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
            print(f"\n🔴 ERRORE: Problema con la paginazione: {str(e)}")
            assert False, "No element was found in the page."
