from selenium.webdriver.common.by import By

class CartPage:
    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, driver):
        self.driver = driver

    def item_names(self):
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item_name")
        return [el.text for el in elements]