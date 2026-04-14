from selenium.webdriver.common.by import By

class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    username = (By.ID, "user-name")
    password = (By.ID, "password")
    login_btn = (By.ID, "login-button")
    error_message = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        self.driver.get("https://www.saucedemo.com/")

    def login(self, user, pwd):
        self.driver.find_element(*self.username).send_keys(user)
        self.driver.find_element(*self.password).send_keys(pwd)
        self.driver.find_element(*self.login_btn).click()

    def get_error_message(self):
        return self.driver.find_element(*self.error_message).text
