import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@allure.feature("Авторизация")
@allure.title("Страница логина загружается")
def test_login_page_load(driver):
    login_page = LoginPage(driver)
    login_page.open()

    assert login_page.login_button().is_displayed()

@allure.feature("Авторизация")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "username",
    ["standard_user", "visual_user", "problem_user", "performance_glitch_user"],
)
def test_successful_login(driver, username):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, "secret_sauce")

    inventory_page = InventoryPage(driver)
    assert inventory_page.title() == "Products"

@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
    ],
)
def test_failed_login(driver, username, password, expected_error):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, password)

    error_text = login_page.error_message()
    assert expected_error in error_text

def test_logout(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    inventory_page.logout()
    
    login_page.wait_until_loaded()
    assert login_page.login_button().is_displayed()