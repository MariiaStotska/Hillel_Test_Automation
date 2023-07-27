import time
import allure
import pytest
from models_for_api_tests.register_post_model import RegisterPostModel
from selenium.common.exceptions import NoSuchElementException
import requests
from pages.profile_page import ProfilePage
from driver import Driver
from pages.login_page import LoginPage
from pages.garage_page import GaragePage
from pages.settings_page import SettingsPage
from pages.register_page import RegisterPage
from datetime import date, timedelta


class TestUserProfile:
    def setup_class(self):
        self.driver = Driver.get_chrome_driver()
        self.login_page = LoginPage()
        self.register_page = RegisterPage()
        self.garage_page = GaragePage()
        self.profile_page = ProfilePage()
        self.settings_page = SettingsPage()
        self.session = requests.session()
        self.register_user_data = RegisterPostModel("Nick", "Fedorchuck", "fedorchuck_nick@gmail.com",
                                                    "Nick1997N", "Nick1997N")
        self.session.post("https://qauto.forstudy.space/api/auth/signup", json=self.register_user_data.__dict__)

    def setup_method(self):
        self.driver.get("https://guest:welcome2qauto@qauto.forstudy.space/")
        self.login_page.get_sign_in_button().click()
        self.login_page.get_email_field().fill_field("fedorchuck_nick@gmail.com")
        self.login_page.get_password_field().fill_field("Nick1997N")
        self.login_page.get_login_button().click()

    @allure.step("Profile page displayed")
    def test_profile_page_displayed(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        assert self.profile_page.get_open_edit_profile_button().is_displayed()

    @allure.step("Profile button is not enabled when selected")
    def test_profile_button_in_dropdown_is_not_enabled_when_selected(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        self.garage_page.get_my_profile_button().click()
        assert not self.profile_page.get_profile_dropdown_menu_button().is_enabled()

    @allure.step("Profile button in side menu is active when selected")
    def test_profile_button_in_side_menu_is_active_when_selected(self):
        profile_settings_side_menu = self.profile_page.get_profile_side_menu_button()
        profile_settings_side_menu.click()
        assert profile_settings_side_menu.is_active()

    def test_default_data_is_displayed_correctly_in_profile_after_signin(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        name = self.register_user_data.name
        last_name = self.register_user_data.lastName
        full_name = f"{name} {last_name}"
        src = 'https://qauto.forstudy.space/public/images/users/default-user.png'
        assert self.profile_page.get_profile_page_user_full_name_title().get_text() == full_name
        assert self.profile_page.get_profile_page_user_photo_img().get_img_source() == src
        try:
            country_title_element = self.profile_page.get_profile_page_user_country_title()
            birthday_title_element = self.profile_page.get_profile_page_user_birthday_title()

            if country_title_element is not None and birthday_title_element is not None:
                assert False, "Test failed. Title elements are present on the page."

        except NoSuchElementException:
            pass
        assert True, "Test passed. Country and birthday elements are not present on the page."

    @allure.step("Edit profile window is opened")
    def test_edit_profile_window_is_opened(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        try:
            assert self.profile_page.get_edit_profile_name_field().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Edit profile window is closed")
    def test_close_edit_profile_window(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        self.profile_page.get_edit_profile_x_button().click()
        assert self.profile_page.get_open_edit_profile_button().is_displayed()

    @allure.step("Save button in edit window is not enabled by default")
    def test_save_button_in_edit_window_is_not_enabled_by_default(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        try:
            assert not self.profile_page.get_edit_profile_save_button().is_enabled()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Name is required alert appears")
    def test_alert_name_is_required_appears(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_name_field().clean_field()
        self.profile_page.get_edit_profile_last_name_field().click()

        try:
            assert self.profile_page.get_edit_profile_name_is_required_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Last name is required alert appears")
    def test_alert_last_name_is_required_appears(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_last_name_field().clean_field()
        self.profile_page.get_edit_profile_name_field().click()

        try:
            assert self.profile_page.get_edit_profile_last_name_is_required_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

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
    def test_not_valid_data_alert_last_name_appears(self, last_name):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_last_name_field().clean_field()
        self.profile_page.get_edit_profile_last_name_field().fill_field(last_name)
        self.profile_page.get_edit_profile_name_field().click()
        try:
            assert self.profile_page.get_edit_profile_last_name_not_valid_data_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

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
    def test_not_valid_data_alert_name_appears(self, name):
        time.sleep(2)
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_name_field().clean_field()
        self.profile_page.get_edit_profile_name_field().fill_field(name)
        self.profile_page.get_edit_profile_last_name_field().click()
        try:
            assert self.profile_page.get_edit_profile_name_not_valid_data_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Data to check name incorrect data alert appears")
    @pytest.mark.parametrize("name", [
        'A',
        'abcabcabcabcabcabcabc'
    ])
    def test_incorrect_data_alert_name_appears(self, name):
        time.sleep(2)
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_name_field().clean_field()
        self.profile_page.get_edit_profile_name_field().fill_field(name)
        self.profile_page.get_edit_profile_last_name_field().click()
        try:
            assert self.profile_page.get_edit_profile_name_incorrect_data_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Data to check last name incorrect data alert appears")
    @pytest.mark.parametrize("last_name", [
        'A',
        'abcabcabcabcabcabcabc'
    ])
    def test_incorrect_data_alert_last_name_appears(self, last_name):
        time.sleep(2)
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_last_name_field().clean_field()
        self.profile_page.get_edit_profile_last_name_field().fill_field(last_name)
        self.profile_page.get_edit_profile_name_field().click()
        try:
            assert self.profile_page.get_edit_profile_last_name_incorrect_data_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Data to fill name field")
    def fill_name_field(self, name):
        self.profile_page.get_edit_profile_name_field().fill_field(name)

    def test_check_name_field_length_and_not_valid_data(self):
        time.sleep(2)
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_name_field().clean_field()
        self.fill_name_field("@")
        self.profile_page.get_edit_profile_last_name_field().click()
        try:
            assert self.profile_page.get_edit_profile_name_incorrect_data_alert().is_displayed()\
                   and self.profile_page.get_edit_profile_name_not_valid_data_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Data to fill last name field")
    def fill_last_name_field(self, last_name):
        self.profile_page.get_edit_profile_last_name_field().fill_field(last_name)

    def test_check_last_name_field_length_and_not_valid_data(self):
        time.sleep(2)
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_last_name_field().clean_field()
        self.fill_last_name_field("@")
        self.profile_page.get_edit_profile_name_field().click()
        try:
            assert self.profile_page.get_edit_profile_last_name_incorrect_data_alert().is_displayed() \
                   and self.profile_page.get_edit_profile_last_name_not_valid_data_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Check save button is not enabled without changes in edit fields")
    def test_save_button_is_not_enabled_without_changes_in_edit_fields(self):
        time.sleep(2)
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_name_field().click()
        self.profile_page.get_edit_profile_last_name_field().click()
        self.profile_page.get_edit_profile_country_field().click()
        self.profile_page.get_edit_profile_birthday_field().click()
        try:
            assert not self.profile_page.get_edit_profile_save_button().is_enabled()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Data to check country field incorrect data alert appears")
    @pytest.mark.parametrize("country", [
        'A',
        'abcabcabcabcabcabcabc'
    ])
    def test_incorrect_data_alert_country_appears(self, country):
        time.sleep(2)
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_country_field().fill_field(country)
        self.profile_page.get_edit_profile_last_name_field().click()
        try:
            assert self.profile_page.get_edit_profile_country_incorrect_data_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Data to check country field not valid data alert appears")
    @pytest.mark.parametrize("country", [
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
    def test_not_valid_data_alert_country_appears(self, country):
        time.sleep(2)
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_country_field().fill_field(country)
        self.profile_page.get_edit_profile_last_name_field().click()
        try:
            assert self.profile_page.get_edit_profile_country_not_valid_data_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Data to fill country field")
    def fill_country_field(self, country):
        self.profile_page.get_edit_profile_country_field().fill_field(country)

    def test_check_country_field_length_and_not_valid_data(self):
        time.sleep(2)
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.fill_country_field("@")
        self.profile_page.get_edit_profile_last_name_field().click()
        try:
            assert self.profile_page.get_edit_profile_country_not_valid_data_alert().is_displayed() \
               and self.profile_page.get_edit_profile_country_incorrect_data_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    def test_save_button_is_enabled_after_clearing_country_field(self):
        time.sleep(2)
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.fill_country_field("USA")
        self.profile_page.get_edit_profile_save_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        self.profile_page.get_edit_profile_country_field().clean_field()

        try:
            assert self.profile_page.get_edit_profile_save_button().is_enabled()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    today = date.today()
    tomorrow_day = today + timedelta(days=1)

    @allure.step("Data to check birthday field with invalid data")
    @pytest.mark.parametrize("birthday", [
        '32.07.1990',
        '00.13.1985',
        '15.00.1985',
        '31.09.2000',
        '20.07.',
        '.07.2023',
        '20.07.2098',
        '20.07.20300',
        '20.11.20',
        '20.07',
        '20/07/1990',
        '15041985',
        '2000-01-01',
        tomorrow_day.strftime('%d.%m.%Y')
    ])
    def test_invalid_data_birthday_field_alert_and_save_button_is_not_enabled(self, birthday):
        time.sleep(2)
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_birthday_field().fill_field(birthday)
        self.profile_page.get_edit_profile_country_field().click()
        try:
            assert not self.profile_page.get_edit_profile_save_button().is_enabled() \
                   and self.profile_page.get_edit_profile_birthday_not_valid_data_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Data to check birthday field with incorrect data")
    @pytest.mark.parametrize("birthday", [
        'abcdefg',
        '12.ab.2013',
        '!@#$%^',
        ' '
    ])
    def test_incorrect_data_birthday_field_alert_and_save_button_is_not_enabled(self, birthday):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_birthday_field().fill_field(birthday)
        self.profile_page.get_edit_profile_country_field().click()
        try:
            assert not self.profile_page.get_edit_profile_save_button().is_enabled() \
                   and self.profile_page.get_edit_profile_birthday_incorrect_data_alert().is_displayed()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    @allure.step("Data to check birthday field with correct data")
    @pytest.mark.parametrize("birthday", [
        '04.07.1990',
        '1.1.2000',
        '15.12.1985',
        today.strftime('%d.%m.%Y')
    ])
    def test_save_button_is_enabled_when_birthday_has_correct_data(self, birthday):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_birthday_field().fill_field(birthday)
        time.sleep(2)
        try:
            assert self.profile_page.get_edit_profile_save_button().is_enabled()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    def test_successful_edit_profile_name(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_name_field().clean_field()
        self.fill_name_field('Mariia')
        last_name = self.register_user_data.lastName
        self.profile_page.get_edit_profile_save_button().click()
        try:
            assert self.profile_page.get_user_profile_has_been_updated_alert().is_displayed()
            assert self.profile_page.get_profile_page_user_full_name_title().get_text() == f'Mariia {last_name}'
        finally:
            self.profile_page.get_open_edit_profile_button().click()
            self.profile_page.get_edit_profile_name_field().clean_field()
            self.profile_page.get_edit_profile_name_field().fill_field(self.register_user_data.name)
            self.profile_page.get_edit_profile_save_button().click()

    def test_successful_edit_profile_last_name(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_last_name_field().clean_field()
        self.fill_last_name_field('Wow')
        name = self.register_user_data.name
        self.profile_page.get_edit_profile_save_button().click()
        try:
            assert self.profile_page.get_user_profile_has_been_updated_alert().is_displayed()
            assert self.profile_page.get_profile_page_user_full_name_title().get_text() == f'{name} Wow'
        finally:
            self.profile_page.get_open_edit_profile_button().click()
            self.profile_page.get_edit_profile_last_name_field().clean_field()
            self.profile_page.get_edit_profile_last_name_field().fill_field(self.register_user_data.lastName)
            self.profile_page.get_edit_profile_save_button().click()

    def test_successful_edit_profile_country(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_country_field().clean_field()
        self.fill_country_field("USA")
        self.profile_page.get_edit_profile_name_field().clean_field()
        self.fill_name_field('Mariia')
        self.profile_page.get_edit_profile_last_name_field().clean_field()
        self.fill_last_name_field('Stotska')
        self.profile_page.get_edit_profile_save_button().click()
        try:
            assert self.profile_page.get_user_profile_has_been_updated_alert().is_displayed()
            assert self.profile_page.get_profile_page_user_country_title().get_text() == 'USA'
        finally:
            self.profile_page.get_open_edit_profile_button().click()
            self.profile_page.get_edit_profile_country_field().clean_field()
            self.profile_page.get_edit_profile_name_field().clean_field()
            self.profile_page.get_edit_profile_name_field().fill_field(self.register_user_data.name)
            self.profile_page.get_edit_profile_last_name_field().clean_field()
            self.profile_page.get_edit_profile_last_name_field().fill_field(self.register_user_data.lastName)
            self.profile_page.get_edit_profile_save_button().click()

    @allure.step("Data to fill birthday field")
    def fill_birthday_field(self, birthday):
        self.profile_page.get_edit_profile_birthday_field().fill_field(birthday)

    def test_successful_edit_profile_birthday(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.fill_birthday_field('08.06.1997')
        self.profile_page.get_edit_profile_name_field().clean_field()
        self.fill_name_field('Mariia')
        self.profile_page.get_edit_profile_last_name_field().clean_field()
        self.fill_last_name_field('Stotska')
        self.profile_page.get_edit_profile_save_button().click()
        try:
            assert self.profile_page.get_user_profile_has_been_updated_alert().is_displayed()
            assert self.profile_page.get_profile_page_user_birthday_title().get_text() == '08.06.1997'
        finally:
            self.profile_page.get_open_edit_profile_button().click()
            self.profile_page.get_edit_profile_birthday_field().clean_field()
            self.profile_page.get_edit_profile_name_field().clean_field()
            self.profile_page.get_edit_profile_name_field().fill_field(self.register_user_data.name)
            self.profile_page.get_edit_profile_last_name_field().clean_field()
            self.profile_page.get_edit_profile_last_name_field().fill_field(self.register_user_data.lastName)
            self.profile_page.get_edit_profile_save_button().click()

    def test_birthday_country_titles_are_not_displayed_on_profile_page_after_clearing(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_birthday_field().clean_field()
        self.fill_birthday_field('08.06.1997')
        self.profile_page.get_edit_profile_country_field().clean_field()
        self.fill_country_field("USA")
        self.profile_page.get_edit_profile_name_field().clean_field()
        self.fill_name_field('Mariia')
        self.profile_page.get_edit_profile_last_name_field().clean_field()
        self.fill_last_name_field('Stotska')
        self.profile_page.get_edit_profile_save_button().click()
        self.profile_page.get_open_edit_profile_button().click()
        self.profile_page.get_edit_profile_birthday_field().clean_field()
        self.profile_page.get_edit_profile_country_field().clean_field()
        self.profile_page.get_edit_profile_name_field().clean_field()
        self.profile_page.get_edit_profile_name_field().fill_field(self.register_user_data.name)
        self.profile_page.get_edit_profile_last_name_field().clean_field()
        self.profile_page.get_edit_profile_last_name_field().fill_field(self.register_user_data.lastName)
        self.profile_page.get_edit_profile_save_button().click()
        time.sleep(5)
        try:
            country_title_element = self.profile_page.get_profile_page_user_country_title()
            birthday_title_element = self.profile_page.get_profile_page_user_birthday_title()

            if country_title_element is not None and birthday_title_element is not None:
                assert False, "Test failed. Title elements are still present on the page."

        except NoSuchElementException:
            pass

    def test_save_button_is_enabled_after_clearing_birthday_field(self):
        self.garage_page.get_my_profile_button().click()
        self.profile_page.get_profile_dropdown_menu_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        time.sleep(2)
        self.profile_page.get_edit_profile_birthday_field().clean_field()
        self.fill_birthday_field("07.05.2001")
        self.profile_page.get_edit_profile_save_button().click()
        time.sleep(2)
        self.profile_page.get_open_edit_profile_button().click()
        self.profile_page.get_edit_profile_birthday_field().clean_field()

        try:
            assert self.profile_page.get_edit_profile_save_button().is_enabled()
        finally:
            self.profile_page.get_edit_profile_x_button().click()

    def teardown_method(self):
        screen_name_using_current_time = time.strftime('%Y%m%d-%H%M%S')
        allure.attach(self.driver.get_screenshot_as_png(), name=screen_name_using_current_time)
        time.sleep(5)
        self.garage_page.get_logout_button_side_menu().click()

    def teardown_class(self):
        time.sleep(5)
        self.login_page.get_sign_in_button().click()
        self.login_page.get_email_field().fill_field("fedorchuck_nick@gmail.com")
        self.login_page.get_password_field().fill_field("Nick1997N")
        self.login_page.get_login_button().click()
        time.sleep(5)
        self.settings_page.get_settings_side_menu_button().click()
        self.settings_page.get_remove_my_account_button().click()
        self.settings_page.get_remove_my_account_window_remove_button().click()
