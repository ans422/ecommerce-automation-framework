from utils.driver_factory import get_driver
from pages.login_page import LoginPage

def test_valid_login():
    driver = get_driver()
    
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

    assert "inventory" in driver.current_url
    
    driver.quit()
