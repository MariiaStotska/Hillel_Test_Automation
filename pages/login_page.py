from selenium.webdriver.common.by import By
from .base_page_with_driver import BasePageWithDriver
from controls.button import Button
from controls.textbox import TextBox
from controls.label import Label
from controls.checkbox import CheckBox


class LoginPage(BasePageWithDriver):
    def __init__(self):
        super().__init__()
        self._sign_in_button = None
        self._close_button = None
        self._login_button = None
        self._email_field = None
        self._password_field = None
        self._remember_me_checkbox = None
        self._email_required_alert = None
        self._password_required_alert = None
        self._email_not_valid_data_alert = None
        self._wrong_email_or_password_alert = None

    def get_sign_in_button(self):
        self._sign_in_button = Button(self._driver.find_element(By.XPATH, "//button[text()='Sign In']"))
        return self._sign_in_button

    def get_close_button(self):
        self._close_button = Button(self._driver.find_element(By.XPATH, "//button[@class='close']"))
        return self._close_button

    def get_login_button(self):
        self._login_button = Button(self._driver.find_element(By.XPATH, "//button[text()='Login']"))
        return self._login_button

    def get_email_field(self):
        self._email_field = TextBox(self._driver.find_element(By.ID, "signinEmail"))
        return self._email_field

    def get_password_field(self):
        self._password_field = TextBox(self._driver.find_element(By.ID, "signinPassword"))
        return self._password_field

    def get_remember_me_checkbox(self):
        self._remember_me_checkbox = CheckBox(self._driver.find_element(By.ID, "remember"))
        return self._remember_me_checkbox

    def get_email_required_alert(self):
        self._email_required_alert = Label(self._driver.find_element(By.XPATH, "//p[text()='Email required']"))
        return self._email_required_alert

    def get_password_required_alert(self):
        self._password_required_alert = Label(self._driver.find_element(By.XPATH, "//p[text()='Password required']"))
        return self._password_required_alert

    def get_email_not_valid_data_alert(self):
        self._email_not_valid_data_alert = Label(self._driver.find_element(By.XPATH,
                                                                           "//p[text()='Email is incorrect']"))
        return self._email_not_valid_data_alert

    def get_wrong_email_or_password_alert(self):
        self._wrong_email_or_password_alert = Label(self._driver.find_element(By.XPATH,
                                                                              "//p[text()='Wrong email or password']"))
        return self._wrong_email_or_password_alert
