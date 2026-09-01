from selenium.webdriver.common.by import By

class LoginPage:
    URL = "https://www.saucedemo.com"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def login_button(self):
        return self.driver.find_element(By.ID, "login-button")