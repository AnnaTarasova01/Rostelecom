from pages import BasePage
from pages import AuthLocators

import time, os

class AuthPage(BasePage):

    def __init__(self, driver, timeout=5):
        super().__init__(driver, timeout)
        url = os.getenv("LOGIN_URL") or "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth/?client_id=lk_onlime&redirect_uri=https%3A%2F%2Fmy.rt.ru%2Fauth%2Fssoredirect%2F&response_type=code&auth_type=standard"
        driver.get(url)
        self.email = driver.find_element(*AuthLocators.AUTH_EMAIL)
        self.passw = driver.find_element(*AuthLocators.AUTH_PASS)
        self.btn = driver.find_element(*AuthLocators.AUTH_BTN)
        time.sleep(3)

    def enter_email(self, value):
        self.email.send_keys(value)

    def enter_pass(self, value):
        self.passw.send_keys(value)

    def btn_click(self):
        self.btn.click()




