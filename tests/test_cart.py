from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

def test_add_to_cart(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("performance_glitch_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    inventory_page.add_first_item_to_cart()

    assert inventory_page.cart_badge_count() == "1"