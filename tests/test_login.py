from pages.login_page import LoginPage

def test_valid_login(driver):
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

    assert "inventory" in driver.current_url

def test_invalid_login(driver):
    login = LoginPage(driver)
    login.open()
    login.login("locked_out_user", "secret_sauce")

    assert "Epic sadface: Sorry, this user has been locked out." in login.get_error_message()
