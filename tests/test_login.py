from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

def test_login_page_load(driver):
    login_page = LoginPage(driver)
    login_page.open()

    assert login_page.login_button().is_displayed()

def test_successful_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    assert inventory_page.title() == "Products"