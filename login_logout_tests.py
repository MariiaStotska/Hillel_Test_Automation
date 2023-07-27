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


class TestLoginLogout:
    def setup_class(self):
        self.driver = Driver.get_chrome_driver()
        self.login_page = LoginPage()
        self.garage_page = GaragePage()
        self.register_page = RegisterPage()
        self.session = requests.session()
        register_user_data = RegisterPostModel("Valeria", "Fedorchuk", "fedorchuck_valeria@gmail.com",
                                               "Valeria1997V", "Valeria1997V")
        self.session.post("https://qauto.forstudy.space/api/auth/signup", json=register_user_data.__dict__)

    def setup_method(self):
        self.driver.get("https://guest:welcome2qauto@qauto.forstudy.space/")

    @allure.step("Check login window is displayed")
    def test_check_login_window(self):
        self.login_page.get_sign_in_button().click()
        assert self.login_page.get_email_field().is_displayed()

    @allure.step("Check login page close button")
    def test_check_login_page_close_button(self):
        self.login_page.get_sign_in_button().click()
        time.sleep(3)
        self.login_page.get_close_button().click()
        assert self.login_page.get_sign_in_button().is_displayed()

    @allure.step("Check login button is enabled")
    def test_check_login_button_is_enabled(self):
        self.login_page.get_sign_in_button().click()
        assert not self.login_page.get_login_button().is_enabled()

    @allure.step("Fill login form with email and password")
    def fill_login_form(self, email, password):
        self.login_page.get_email_field().fill_field(email)
        self.login_page.get_password_field().fill_field(password)

    def test_check_successful_login_with_unchecked_remember_me_button(self):
        self.login_page.get_sign_in_button().click()
        self.fill_login_form('fedorchuck_valeria@gmail.com', 'Valeria1997V')
        assert not self.login_page.get_remember_me_checkbox().is_checked()
        self.login_page.get_login_button().click()
        assert self.garage_page.get_my_profile_button().is_displayed()
        self.garage_page.get_my_profile_button().click()
        self.garage_page.get_logout_button().click()

    def test_check_successful_login_with_checked_remember_me_checkbox(self):
        self.login_page.get_sign_in_button().click()
        self.fill_login_form('fedorchuck_valeria@gmail.com', 'Valeria1997V')
        self.login_page.get_remember_me_checkbox().check()
        assert self.login_page.get_remember_me_checkbox().is_checked()
        self.login_page.get_login_button().click()
        assert self.garage_page.get_successful_login_alert().is_displayed()
        self.garage_page.get_my_profile_button().click()
        self.garage_page.get_logout_button().click()

    def test_check_login_with_not_registered_user(self):
        self.login_page.get_sign_in_button().click()
        self.fill_login_form('fedorchuck_val@gmail.com', 'Vasyl1993V')
        self.login_page.get_login_button().click()
        assert self.login_page.get_wrong_email_or_password_alert().is_displayed()

    @allure.step("Check password is required alert appears")
    def test_check_password_is_required(self):
        self.login_page.get_sign_in_button().click()
        self.login_page.get_password_field().click()
        self.login_page.get_email_field().click()
        assert self.login_page.get_password_required_alert().is_displayed()

    @allure.step("Check email is required alert appears")
    def test_check_email_is_required(self):
        self.login_page.get_sign_in_button().click()
        self.login_page.get_email_field().click()
        self.login_page.get_password_field().click()
        assert self.login_page.get_email_required_alert().is_displayed()

    @allure.step("Check email incorrect alert appears")
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
        self.login_page.get_email_field().fill_field(email)
        self.login_page.get_password_field().click()
        assert self.login_page.get_email_not_valid_data_alert().is_displayed()

    def test_user_logout(self):
        self.login_page.get_sign_in_button().click()
        self.fill_login_form('fedorchuck_valeria@gmail.com', 'Valeria1997V')
        self.login_page.get_login_button().click()
        self.garage_page.get_my_profile_button().click()
        self.garage_page.get_logout_button().click()
        assert self.login_page.get_sign_in_button().is_displayed()

    @allure.step("Check user logout via side menu")
    def test_user_logout_via_side_menu(self):
        self.login_page.get_sign_in_button().click()
        self.fill_login_form('fedorchuck_valeria@gmail.com', 'Valeria1997V')
        self.login_page.get_login_button().click()
        self.garage_page.get_my_profile_button().click()
        self.garage_page.get_logout_button_side_menu().click()
        assert self.login_page.get_sign_in_button().is_displayed()

    def teardown_method(self):
        screen_name_using_current_time = time.strftime('%Y%m%d-%H%M%S')
        allure.attach(self.driver.get_screenshot_as_png(), name=screen_name_using_current_time)

    def teardown_class(self):
        sign_in_data = SigninPostModel("fedorchuck_valeria@gmail.com", "Valeria1997V", "False")
        self.session.post("https://qauto.forstudy.space/api/auth/signin", json=sign_in_data.__dict__)
        self.session.delete("https://qauto.forstudy.space/api/users")
