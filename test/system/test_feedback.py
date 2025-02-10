import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def driver():
    """Setup del WebDriver per Selenium."""
    driver = webdriver.Chrome()  # Assicurati di avere chromedriver installato
    driver.implicitly_wait(10)  # Imposta il timeout implicito
    yield driver
    driver.quit()  # Chiude il browser dopo il test

def test_feedback_submission(driver):
    """
    Test di sistema per la feedback_service.
    1. Caricare il file
    2. Cliccare 'Analyze' sulla prima user story
    3. Cliccare 'Valuta'
    4. Selezionare 5 stelle per il dominio e 4 per il task
    5. Premere 'Submit Rating'
    """

    driver.get("http://localhost:5173/")

    # **Step 1: Caricare il file**
    file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
    file_input.send_keys("/path/to/your/file.xlsx")  # Cambia con il path del file
    driver.find_element(By.CSS_SELECTOR, ".load").click()

    # Attendi che le user stories vengano caricate
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
    )

    # **Step 2: Cliccare "Analyze" sulla prima user story**
    analyze_button = driver.find_element(By.CSS_SELECTOR, "table tbody tr:first-child .analyze")
    analyze_button.click()

    # **Step 3: Cliccare "Valuta" per aprire la finestra di valutazione**
    rate_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.rating"))
    )
    rate_button.click()

    # **Step 4: Selezionare 5 stelle per il dominio e 4 per il task**
    stars_domain = driver.find_elements(By.CSS_SELECTOR, ".rating-container span")
    stars_domain[4].click()  # 5 stelle sul dominio

    stars_task = driver.find_elements(By.CSS_SELECTOR, ".rating-container span")
    stars_task[3].click()  # 4 stelle sul task

    # **Step 5: Premere "Submit Rating"**
    submit_button = driver.find_element(By.CSS_SELECTOR, ".button.submit-rating")
    submit_button.click()

    # **Verifica del successo**
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert "Rating submitted successfully!" in alert.text
    alert.accept()
