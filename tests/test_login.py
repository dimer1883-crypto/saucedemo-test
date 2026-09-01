from pages.login_page import LoginPage

def test_login_page_load(driver):
    login_page = LoginPage(driver)
    login_page.open()

    assert login_page.login_button().is_displayed()