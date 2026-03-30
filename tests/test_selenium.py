import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

APP_URL = "http://localhost:8501"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,800")

    service = Service(ChromeDriverManager().install())
    d = webdriver.Chrome(service=service, options=options)
    d.implicitly_wait(10)
    yield d
    d.quit()

def wait_for_app(driver, timeout=30):
    """Wait until Streamlit app is loaded."""
    for _ in range(timeout):
        try:
            driver.get(APP_URL)
            if "SecureApp" in driver.title or driver.find_elements(By.TAG_NAME, "h1"):
                return True
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError(f"App not reachable at {APP_URL} after {timeout}s")

class TestSecureApp:

    def test_app_loads(self, driver):
        wait_for_app(driver)
        assert "Security" in driver.page_source or "SecureApp" in driver.title

    def test_title_visible(self, driver):
        driver.get(APP_URL)
        wait = WebDriverWait(driver, 15)
        heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        assert "Security" in heading.text

    def test_password_tab_present(self, driver):
        driver.get(APP_URL)
        time.sleep(3)
        page = driver.page_source
        assert "Check Password" in page or "password" in page.lower()

    def test_generate_tab_present(self, driver):
        driver.get(APP_URL)
        time.sleep(3)
        assert "Generate" in driver.page_source

    def test_history_tab_present(self, driver):
        driver.get(APP_URL)
        time.sleep(3)
        assert "History" in driver.page_source

    def test_no_js_errors(self, driver):
        driver.get(APP_URL)
        time.sleep(3)
        logs = driver.get_log("browser")
        severe = [l for l in logs if l.get("level") == "SEVERE"]
        # Streamlit sometimes logs non-critical errors — filter known false positives
        real_errors = [l for l in severe if "favicon" not in l.get("message", "")]
        assert len(real_errors) == 0