from selenium.webdriver.common.by import By
from .base_page_with_driver import BasePageWithDriver
from controls.button import Button
from controls.textbox import TextBox
from controls.label import Label


class SettingsPage(BasePageWithDriver):
    def __init__(self):
        super().__init__()
        self._settings_side_menu_button = None
        self._settings_dropdown_menu_button = None
        self._usd_button = None
        self._uah_button = None
        self._gbp_button = None
        self._eur_button = None
        self._pln_button = None
        self._km_button = None
        self._ml_button = None
        self._currency_changed_alert = None
        self._units_of_distance_changed_alert = None
        self._new_email_address_field = None
        self._change_email_password_field = None
        self._email_required_alert = None
        self._email_is_incorrect_alert = None
        self._password_required_alert = None
        self._wrong_password_alert = None
        self._email_has_been_changed_alert = None
        self._email_should_not_be_the_same_alert = None
        self._old_password_field = None
        self._new_password_field = None
        self._re_enter_new_password_field = None
        self._old_password_required_alert = None
        self._new_password_required_alert = None
        self._re_enter_password_required_alert = None
        self._new_re_enter_passwords_incorrect_alert = None
        self._passwords_do_not_match_alert = None
        self._new_password_should_not_be_the_same_alert = None
        self._password_has_been_changed_alert = None
        self._remove_my_account_button = None
        self._remove_my_account_window_x_button = None
        self._remove_my_account_window_cancel_button = None
        self._remove_my_account_window_remove_button = None
        self._user_account_has_been_removed_alert = None
        self._change_email_button = None
        self._change_password_button = None
        self._email_already_exists_alert = None

    def get_settings_side_menu_button(self):
        self._settings_side_menu_button = Button(self._driver.find_element(
            By.XPATH, "//a[@class='btn btn-white btn-sidebar sidebar_btn' and contains(text(), 'Settings')]"))
        return self._settings_side_menu_button

    def get_settings_dropdown_menu_button(self):
        self._settings_dropdown_menu_button = Button(self._driver.find_element(
            By.XPATH, "//a[text()='Settings']"))
        return self._settings_dropdown_menu_button

    def get_usd_button(self):
        self._usd_button = Button(self._driver.find_element(By.XPATH, "//button[text()='USD']"))
        return self._usd_button

    def get_uah_button(self):
        self._uah_button = Button(self._driver.find_element(By.XPATH, "//button[text()='UAH']"))
        return self._uah_button

    def get_gbp_button(self):
        self._gbp_button = Button(self._driver.find_element(By.XPATH, "//button[text()='GBP']"))
        return self._gbp_button

    def get_eur_button(self):
        self._eur_button = Button(self._driver.find_element(By.XPATH, "//button[text()='EUR']"))
        return self._eur_button

    def get_pln_button(self):
        self._pln_button = Button(self._driver.find_element(By.XPATH, "//button[text()='PLN']"))
        return self._pln_button

    def get_km_button(self):
        self._km_button = Button(self._driver.find_element(By.XPATH, "//button[text()='km']"))
        return self._km_button

    def get_ml_button(self):
        self._ml_button = Button(self._driver.find_element(By.XPATH, "//button[text()='ml']"))
        return self._ml_button

    def get_currency_changed_alert(self):
        self._currency_changed_alert = Label(self._driver.find_element(By.XPATH, "//p[text()='Currency changed']"))
        return self._currency_changed_alert

    def get_units_of_distance_changed_alert(self):
        self._units_of_distance_changed_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Units of distance changed']"))
        return self._units_of_distance_changed_alert

    def get_new_email_address_field(self):
        self._new_email_address_field = TextBox(self._driver.find_element(By.ID, "emailChangeEmail"))
        return self._new_email_address_field

    def get_change_email_password_field(self):
        self._change_email_password_field = TextBox(self._driver.find_element(By.ID, "emailChangePassword"))
        return self._change_email_password_field

    def get_email_required_alert(self):
        self._email_required_alert = Label(self._driver.find_element(By.XPATH, "//p[text()='Email required']"))
        return self._email_required_alert

    def get_email_is_incorrect_alert(self):
        self._email_is_incorrect_alert = Label(self._driver.find_element(By.XPATH, "//p[text()='Email is incorrect']"))
        return self._email_is_incorrect_alert

    def get_password_required_alert(self):
        self._password_required_alert = Label(self._driver.find_element(By.XPATH, "//p[text()='Password required']"))
        return self._password_required_alert

    def get_wrong_password_alert(self):
        self._wrong_password_alert = Label(self._driver.find_element(By.XPATH, "//p[text()='Wrong password']"))
        return self._wrong_password_alert

    def get_email_has_been_changed_alert(self):
        self._email_has_been_changed_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Email has been changed']"))
        return self._email_has_been_changed_alert

    def get_email_should_not_be_the_same_alert(self):
        self._email_should_not_be_the_same_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='The email should not be the same']"))
        return self._email_should_not_be_the_same_alert

    def get_old_password_field(self):
        self._old_password_field = TextBox(self._driver.find_element(By.ID, "passwordChangeOldPassword"))
        return self._old_password_field

    def get_new_password_field(self):
        self._new_password_field = TextBox(self._driver.find_element(By.ID, "passwordChangePassword"))
        return self._new_password_field

    def get_re_enter_new_password_field(self):
        self._re_enter_new_password_field = TextBox(self._driver.find_element(By.ID, "passwordChangeRepeatPassword"))
        return self._re_enter_new_password_field

    def get_old_password_required_alert(self):
        self._old_password_required_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Old password required']"))
        return self._old_password_required_alert

    def get_new_password_required_alert(self):
        self._new_password_required_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='New password required']"))
        return self._new_password_required_alert

    def get_re_enter_password_required_alert(self):
        self._re_enter_password_required_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Re-enter password required']"))
        return self._re_enter_password_required_alert

    def get_new_re_enter_passwords_incorrect_alert(self):
        self._new_re_enter_passwords_incorrect_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Password has to be from 8 to 15 characters long and contain at least "
                      "one integer, one capital, and one small letter']"))
        return self._new_re_enter_passwords_incorrect_alert

    def get_passwords_do_not_match_alert(self):
        self._passwords_do_not_match_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Passwords do not match']"))
        return self._passwords_do_not_match_alert

    def get_new_password_should_not_be_the_same_alert(self):
        self._new_password_should_not_be_the_same_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='New password should not be the same']"))
        return self._new_password_should_not_be_the_same_alert

    def get_password_has_been_changed_alert(self):
        self._password_has_been_changed_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Password has been changed']"))
        return self._password_has_been_changed_alert

    def get_remove_my_account_button(self):
        self._remove_my_account_button = Button(self._driver.find_element(
            By.XPATH, "//button[text()='Remove my account']"))
        return self._remove_my_account_button

    def get_remove_my_account_window_x_button(self):
        self._remove_my_account_window_x_button = Button(self._driver.find_element(
            By.XPATH, "//button[@class='close']"))
        return self._remove_my_account_window_x_button

    def get_remove_my_account_window_cancel_button(self):
        self._remove_my_account_window_cancel_button = Button(self._driver.find_element(
            By.XPATH, "//button[text()='Cancel']"))
        return self._remove_my_account_window_cancel_button

    def get_remove_my_account_window_remove_button(self):
        self._remove_my_account_window_remove_button = Button(self._driver.find_element(
            By.XPATH, "//button[text()='Remove']"))
        return self._remove_my_account_window_remove_button

    def get_user_account_has_been_removed_alert(self):
        self._user_account_has_been_removed_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='User account has been removed']"))
        return self._user_account_has_been_removed_alert

    def get_change_email_button(self):
        self._change_email_button = Button(self._driver.find_element(By.XPATH, "//button[text()='Change email']"))
        return self._change_email_button

    def get_email_already_exists_alert(self):
        self._email_already_exists_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Email already exists']"))
        return self._email_already_exists_alert

    def get_change_password_button(self):
        self._change_password_button = Button(self._driver.find_element(By.XPATH, "//button[text()='Change password']"))
        return self._change_password_button
