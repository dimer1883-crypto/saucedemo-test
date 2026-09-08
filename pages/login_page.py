from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://www.saucedemo.com"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.driver.find_element(By.ID, "user-name").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.login_button().click()

    def login_button(self):
        return self.driver.find_element(By.ID, "login-button")

    def error_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text

    def wait_until_loaded(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login-button"))
        )