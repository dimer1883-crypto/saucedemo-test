
from selenium import webdriver
from selenium.webdriver.common.by import By
def test_login_page_load():
    driver = webdriver.Chrome()
    driver.get("http://www.saucedemo.com")
    login_button = driver.find_element(By.ID, "login-button")
    assert login_button.is_displayed()
    driver.quit()