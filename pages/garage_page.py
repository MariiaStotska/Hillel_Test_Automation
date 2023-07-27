from selenium.webdriver.common.by import By
from .base_page_with_driver import BasePageWithDriver
from controls.button import Button
from controls.label import Label


class GaragePage(BasePageWithDriver):
    def __init__(self):
        super().__init__()
        self._my_profile_button = None
        self._logout_button = None
        self._successful_login_alert = None
        self._logout_button_side_menu = None

    def get_my_profile_button(self):
        self._my_profile_button = Button(self._driver.find_element(By.ID, "userNavDropdown"))
        return self._my_profile_button

    def get_logout_button(self):
        self._logout_button = Button(self._driver.find_element(By.XPATH, "//button[text()='Logout']"))
        return self._logout_button

    def get_successful_login_alert(self):
        self._successful_login_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='You have been successfully logged in']"))
        return self._successful_login_alert

    def get_logout_button_side_menu(self):
        self._logout_button_side_menu = Button(self._driver.find_element(By.XPATH, "//*[text()=' Log out ']"))
        return self._logout_button_side_menu
