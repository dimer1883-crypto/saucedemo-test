import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

def test_login_page_load(driver):
    login_page = LoginPage(driver)
    login_page.open()

    assert login_page.login_button().is_displayed()

@pytest.mark.parametrize(
        "username",
        ["standard_user", "visual_user", "problem_user"],
)
def test_successful_login(driver, username):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, "secret_sauce")

    inventory_page = InventoryPage(driver)
    assert inventory_page.title() == "Products"

def test_failed_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "wrong_password")

    error_text = login_page.error_message()
    assert "Username and password do not match" in error_text