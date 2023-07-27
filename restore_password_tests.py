import time
import pytest
from models_for_api_tests.register_post_model import RegisterPostModel
from models_for_api_tests.signin_post_model import SigninPostModel
import requests
from driver import Driver
from pages.login_page import LoginPage
from pages.garage_page import GaragePage
import allure
from pages.forgot_password_page import ForgotPasswordPage


class TestRestorePassword:
    def setup_class(self):
        self.driver = Driver.get_chrome_driver()
        self.login_page = LoginPage()
        self.garage_page = GaragePage()
        self.forgot_password_page = ForgotPasswordPage()
        self.session = requests.session()
        register_user_data = RegisterPostModel("Kaila", "Fedorchuk", "fedorchuck_kaila@gmail.com",
                                               "Kaila1997M", "Kaila1997M")
        self.session.post("https://qauto.forstudy.space/api/auth/signup", json=register_user_data.__dict__)

    def setup_method(self):
        self.driver.get("https://guest:welcome2qauto@qauto.forstudy.space/")

    def test_check_forgot_password_window(self):
        self.login_page.get_sign_in_button().click()
        self.forgot_password_page.get_forgot_password_button().click()
        assert self.forgot_password_page.get_email_field_in_forgot_password_page().is_displayed()

    def test_check_forgot_password_page_close_button(self):
        self.login_page.get_sign_in_button().click()
        self.forgot_password_page.get_forgot_password_button().click()
        time.sleep(3)
        self.forgot_password_page.get_close_forgot_password_page_button().click()
        assert self.login_page.get_sign_in_button().is_displayed()

    def test_check_login_button_is_enabled(self):
        self.login_page.get_sign_in_button().click()
        self.forgot_password_page.get_forgot_password_button().click()
        assert not self.login_page.get_login_button().is_enabled()

    @allure.step("Fill email field in 'Forgot Password' page")
    def fill_email_field_in_forgot_password_page(self, email):
        self.forgot_password_page.get_email_field_in_forgot_password_page().fill_field(email)

    def test_successful_send_restore_access(self):
        self.login_page.get_sign_in_button().click()
        self.forgot_password_page.get_forgot_password_button().click()
        time.sleep(5)
        self.fill_email_field_in_forgot_password_page('fedorchuck_kaila@gmail.com')
        self.forgot_password_page.get_send_button().click()
        assert self.forgot_password_page.get_successful_alert_instructions_are_sent().is_displayed()

    @allure.step('Data to check email is required alert')
    def test_check_email_is_required(self):
        self.login_page.get_sign_in_button().click()
        self.forgot_password_page.get_forgot_password_button().click()
        time.sleep(1)
        self.forgot_password_page.get_email_field_in_forgot_password_page().click()
        self.driver.execute_script("document.activeElement.blur();")
        assert self.forgot_password_page.get_email_required_alert().is_displayed()

    @allure.step('Data to check email incorrect alerts')
    @pytest.mark.parametrize("email", [
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
    def test_check_email_incorrect_data(self, email):
        self.login_page.get_sign_in_button().click()
        self.forgot_password_page.get_forgot_password_button().click()
        time.sleep(3)
        self.forgot_password_page.get_email_field_in_forgot_password_page().fill_field(email)
        self.driver.execute_script("document.activeElement.blur();")
        assert self.forgot_password_page.get_email_not_valid_data_alert().is_displayed()

    def teardown_method(self):
        screen_name_using_current_time = time.strftime('%Y%m%d-%H%M%S')
        allure.attach(self.driver.get_screenshot_as_png(), name=screen_name_using_current_time)

    def teardown_class(self):
        sign_in_data = SigninPostModel("fedorchuck_maya@gmail.com", "Maya1997M", "False")
        self.session.post("https://qauto.forstudy.space/api/auth/signin", json=sign_in_data.__dict__)
        self.session.delete("https://qauto.forstudy.space/api/users")
