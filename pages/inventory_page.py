from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, driver):
        self.driver = driver

    def title(self):
        return self.driver.find_element(By.CLASS_NAME, "title").text

    def add_first_item_to_cart(self):
        self.driver.find_element(By.CSS_SELECTOR, ".inventory_item button").click()

    def cart_badge_count(self):
        badge = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".shopping_cart_badge"))
        )
        return badge.text
    
    def open_cart(self):
        self.driver.find_element(By.CSS_SELECTOR, ".shopping_cart_link").click()

    def logout(self):
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()
        logout_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logout_link.click()