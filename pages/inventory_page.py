from selenium.webdriver.common.by import By

class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, driver):
        self.driver = driver

    def title(self):
        return self.driver.find_element(By.CLASS_NAME, "title").text