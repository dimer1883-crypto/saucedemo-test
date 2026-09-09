import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

@allure.feature("Корзина")
def test_add_to_cart(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("performance_glitch_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    inventory_page.add_first_item_to_cart()

    assert inventory_page.cart_badge_count() == "1"

@allure.feature("Корзина")
def test_cart_contains_added_item(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    inventory_page.add_first_item_to_cart()
    inventory_page.open_cart()

    cart_page = CartPage(driver)
    assert "Sauce Labs Backpack" in cart_page.item_names()