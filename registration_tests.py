import time
import pytest
import allure
from models_for_api_tests.register_post_model import RegisterPostModel
from models_for_api_tests.signin_post_model import SigninPostModel
import requests
from driver import Driver
from pages.login_page import LoginPage
from pages.garage_page import GaragePage
from pages.register_page import RegisterPage
from pages.settings_page import SettingsPage


class TestRegistration:
    def setup_class(self):
        self.driver = Driver.get_chrome_driver()
        self.login_page = LoginPage()
        self.garage_page = GaragePage()
        self.register_page = RegisterPage()
        self.settings_page = SettingsPage()
        self.session = requests.session()

    def setup_method(self):
        self.driver.get("https://guest:welcome2qauto@qauto.forstudy.space/")

    @allure.step("Check registration window is displayed")
    def test_check_registration_window(self):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        assert self.register_page.get_name_field().is_displayed()

    @allure.step("Data to fill fields of registration form")
    def fill_all_fields_of_registration_form(self, name, last_name, email, password, repeat_password):
        self.register_page.get_name_field().fill_field(name)
        self.register_page.get_last_name_field().fill_field(last_name)
        self.register_page.get_email_field().fill_field(email)
        self.register_page.get_password_field().fill_field(password)
        self.register_page.get_repeat_password_field().fill_field(repeat_password)

    def test_check_register_button_is_enabled(self):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.fill_all_fields_of_registration_form('M', 'Fedorchuk', 'fedorchuck_maryna@gmail.com', 'Maryna1997M',
                                                  'Maryna1997M')
        assert not self.register_page.get_register_button().is_enabled()

    @allure.step("Check name is required alert appears")
    def test_check_name_is_required(self):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.register_page.get_name_field().click()
        self.register_page.get_last_name_field().click()
        assert self.register_page.get_name_required_alert().is_displayed()

    @allure.step("Check last name is required alert appears")
    def test_check_last_name_is_required(self):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.register_page.get_last_name_field().click()
        self.register_page.get_name_field().click()
        assert self.register_page.get_last_name_required_alert().is_displayed()

    @allure.step("Check email is required alert appears")
    def test_check_email_is_required(self):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.register_page.get_email_field().click()
        self.register_page.get_name_field().click()
        assert self.register_page.get_email_required_alert().is_displayed()

    @allure.step("Data to check email is incorrect alert appears")
    @pytest.mark.parametrize("email_address", [
        '@@hm.co',
        ' test@test.com',
        'test@test.com ',
        'invalid.email@domain',
        'invalidgmail.com',
        'inv alid@gmail.com',
        '@example.com',
        'user@',
        'user@.com',
        'user@example..com'
    ])
    def test_check_email_incorrect(self, email_address):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.register_page.get_email_field().fill_field(email_address)
        self.register_page.get_name_field().click()
        assert self.register_page.get_email_not_valid_data_alert().is_displayed()

    @allure.step(" Check password is required alert appears")
    def test_check_password_is_required(self):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.register_page.get_password_field().click()
        self.register_page.get_name_field().click()
        assert self.register_page.get_password_required_alert().is_displayed()

    @allure.step("Check repeat password is required alert appears")
    def test_check_repeat_password_is_required(self):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.register_page.get_repeat_password_field().click()
        self.register_page.get_name_field().click()
        assert self.register_page.get_repeat_password_required_alert().is_displayed()

    @allure.step("Data to check name field length")
    @pytest.mark.parametrize("name", [
        'A',
        'abcabcabcabcabcabcabc'
    ])
    def test_check_name_field_length(self, name):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.register_page.get_name_field().fill_field(name)
        self.register_page.get_last_name_field().click()
        assert self.register_page.get_name_not_valid_length_alert().is_displayed()

    @allure.step("Data to check last name field length")
    @pytest.mark.parametrize("last_name", [
        'A',
        'abcabcabcabcabcabcabc'
    ])
    def test_check_last_name_field_length(self, last_name):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.register_page.get_last_name_field().fill_field(last_name)
        self.register_page.get_name_field().click()
        assert self.register_page.get_last_name_not_valid_length_alert().is_displayed()

    @allure.step("Data to check name not valid data alert appears")
    @pytest.mark.parametrize("name", [
        '@@',
        '##',
        '!!',
        '$$',
        '**',
        '::',
        '()',
        '  ',
        '..',
        ',,',
        '??',
        '--',
        '45'
    ])
    def test_check_name_not_valid_data(self, name):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.register_page.get_name_field().fill_field(name)
        self.register_page.get_last_name_field().click()
        assert self.register_page.get_name_not_valid_data_alert().is_displayed()

    @allure.step("Data to check last name not valid data alert appears")
    @pytest.mark.parametrize("last_name", [
        '@@',
        '##',
        '!!',
        '$$',
        '**',
        '::',
        '()',
        '  ',
        '..',
        ',,',
        '??',
        '--',
        '45'
    ])
    def test_check_last_name_not_valid_data(self, last_name):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.register_page.get_last_name_field().fill_field(last_name)
        self.register_page.get_name_field().click()
        assert self.register_page.get_last_name_not_valid_data_alert().is_displayed()

    @allure.step("Data to fill name field")
    def fill_name_field(self, name):
        self.register_page.get_name_field().fill_field(name)

    def test_check_name_field_length_and_not_valid_data(self):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.fill_name_field('@')
        self.register_page.get_last_name_field().click()
        assert self.register_page.get_name_not_valid_length_alert().is_displayed() \
               and self.register_page.get_name_not_valid_data_alert().is_displayed()

    @allure.step("Data to fill last name field")
    def fill_last_name_field(self, last_name):
        self.register_page.get_last_name_field().fill_field(last_name)

    def test_check_last_name_field_length_and_not_valid_data(self):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.fill_last_name_field('@')
        self.register_page.get_name_field().click()
        assert self.register_page.get_last_name_not_valid_length_alert().is_displayed() \
               and self.register_page.get_last_name_not_valid_data_alert().is_displayed()

    @allure.step("Data to check incorrect password alert appears")
    @pytest.mark.parametrize("password", [
        'password',
        'PASSWORD',
        '12345678',
        'PASSWOR8',
        'passwor8',
        'PASSWORd',
        'PASSWORD123456ppp',
        '@#$%^&*()*'
    ])
    def test_check_incorrect_password_field(self, password):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.register_page.get_password_field().fill_field(password)
        self.register_page.get_name_field().click()
        assert self.register_page.get_password_repeat_password_not_valid_data_alert().is_displayed()

    @allure.step("Data to check incorrect repeat password alert appears")
    @pytest.mark.parametrize("repeat_password", [
        'password',
        'PASSWORD',
        '12345678',
        'PASSWOR8',
        'passwor8',
        'PASSWORd',
        'PASSWORD123456ppp',
        '@#$%^&*()*'
    ])
    def test_check_incorrect_repeat_password_field(self, repeat_password):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.register_page.get_repeat_password_field().fill_field(repeat_password)
        self.register_page.get_name_field().click()
        assert self.register_page.get_password_repeat_password_not_valid_data_alert().is_displayed()

    @allure.step("Data to fill password field and repeat password field")
    def fill_password_and_repeat_password_fields(self, password, repeat_password):
        self.register_page.get_password_field().fill_field(password)
        self.register_page.get_repeat_password_field().fill_field(repeat_password)

    def test_check_passwords_do_not_match(self):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.fill_password_and_repeat_password_fields('passwo2P', 'passwo2PA')
        self.register_page.get_name_field().click()
        assert self.register_page.get_passwords_do_not_match_alert().is_displayed()

    @allure.step("Check register page close button")
    def test_check_register_page_close_button(self):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        time.sleep(5)
        self.register_page.get_close_button().click()
        assert self.login_page.get_sign_in_button().is_displayed()

    @allure.step('Data for registering user via model')
    def user_data_create(self, name, last_name, email, password, repeat_password):
        return RegisterPostModel(name, last_name, email, password, repeat_password)

    def test_check_user_exists(self):
        register_user_data = self.user_data_create("Maryna", "Fedorchuk", "fedorchuck_maryna@gmail.com",
                                                   "Maryna1997M", "Maryna1997M")
        self.session.post("https://qauto.forstudy.space/api/auth/signup", json=register_user_data.__dict__)
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.fill_all_fields_of_registration_form("Maryna", "Fedorchuk", "fedorchuck_maryna@gmail.com",
                                                  "Maryna1997M", "Maryna1997M")
        self.register_page.get_register_button().click()
        try:
            assert self.register_page.get_user_exists_alert().is_displayed()
        finally:
            sign_in_data = SigninPostModel("fedorchuck_maryna@gmail.com", "Maryna1997M", "False")
            self.session.post("https://qauto.forstudy.space/api/auth/signin", json=sign_in_data.__dict__)
            self.session.delete("https://qauto.forstudy.space/api/users")

    @allure.step("Check successful registration")
    def test_check_successful_registration(self):
        self.login_page.get_sign_in_button().click()
        self.register_page.get_registration_button().click()
        self.fill_all_fields_of_registration_form('Maryna', 'Fedorchuk', 'fedorchuck_maryna@gmail.com',
                                                  'Maryna1997M', 'Maryna1997M')
        self.register_page.get_register_button().click()
        try:
            assert self.garage_page.get_my_profile_button().is_displayed()
        finally:
            time.sleep(3)
            self.settings_page.get_settings_side_menu_button().click()
            self.settings_page.get_remove_my_account_button().click()
            self.settings_page.get_remove_my_account_window_remove_button().click()

    def teardown_method(self):
        screen_name_using_current_time = time.strftime('%Y%m%d-%H%M%S')
        allure.attach(self.driver.get_screenshot_as_png(), name=screen_name_using_current_time)

    def teardown_class(self):
        pass
