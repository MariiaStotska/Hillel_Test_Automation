from selenium.webdriver.common.by import By
from .base_page_with_driver import BasePageWithDriver
from controls.button import Button
from controls.label import Label
from controls.textbox import TextBox


class ForgotPasswordPage(BasePageWithDriver):
    def __init__(self):
        super().__init__()
        self._forgot_password_button = None
        self._close_forgot_password_page_button = None
        self._send_button = None
        self._email_field_in_forgot_password_page = None
        self._email_required_alert = None
        self._email_not_valid_data_alert = None
        self._successful_alert_instructions_are_sent = None

    def get_forgot_password_button(self):
        self._forgot_password_button = Button(self._driver.find_element(By.XPATH, "//button[text()='Forgot password']"))
        return self._forgot_password_button

    def get_close_forgot_password_page_button(self):
        self._close_forgot_password_page_button = Button(self._driver.find_element(By.XPATH,
                                                                                   "//button[@class='close']"))
        return self._close_forgot_password_page_button

    def get_send_button(self):
        self._send_button = Button(self._driver.find_element(By.XPATH, "//button[text()='Send']"))
        return self._send_button

    def get_email_field_in_forgot_password_page(self):
        self._email_field_in_forgot_password_page = TextBox(self._driver.find_element(By.XPATH,
                                                                                      "//input[@name='email']"))
        return self._email_field_in_forgot_password_page

    def get_email_required_alert(self):
        self._email_required_alert = Label(self._driver.find_element(By.XPATH, "//p[text()='Email required']"))
        return self._email_required_alert

    def get_email_not_valid_data_alert(self):
        self._email_not_valid_data_alert = Label(self._driver.find_element(By.XPATH,
                                                                           "//p[text()='Email is incorrect']"))
        return self._email_not_valid_data_alert

    def get_successful_alert_instructions_are_sent(self):
        self._successful_alert_instructions_are_sent = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Email with restore instructions was sent']"))
        return self._successful_alert_instructions_are_sent
