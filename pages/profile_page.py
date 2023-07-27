from selenium.webdriver.common.by import By
from .base_page_with_driver import BasePageWithDriver
from controls.button import Button
from controls.textbox import TextBox
from controls.label import Label
from controls.image_box import ImageBox


class ProfilePage(BasePageWithDriver):
    def __init__(self):
        super().__init__()
        self._profile_side_menu_button = None
        self._profile_dropdown_menu_button = None
        self._open_edit_profile_button = None
        self._profile_page_user_full_name_title = None
        self._profile_page_user_country_title = None
        self._profile_page_user_birthday_title = None
        self._profile_page_user_photo_img = None
        self._edit_profile_x_button = None
        self._edit_profile_save_button = None
        self._edit_profile_name_field = None
        self._edit_profile_name_is_required_alert = None
        self._edit_profile_name_not_valid_data_alert = None
        self._edit_profile_name_incorrect_data_alert = None
        self._edit_profile_last_name_field = None
        self._edit_profile_last_name_is_required_alert = None
        self._edit_profile_last_name_not_valid_data_alert = None
        self._edit_profile_last_name_incorrect_data_alert = None
        self._user_profile_has_been_updated_alert = None
        self._edit_profile_birthday_field = None
        self._edit_profile_country_field = None
        self._edit_profile_country_not_valid_data_alert = None
        self._edit_profile_birthday_not_valid_data_alert = None
        self._edit_profile_country_incorrect_data_alert = None
        self._edit_profile_birthday_incorrect_data_alert = None
        self._edit_profile_photo_select_field = None

    def get_profile_side_menu_button(self):
        self._profile_side_menu_button = Button(self._driver.find_element(
            By.XPATH, "//a[@class='btn btn-white btn-sidebar sidebar_btn -profile']"))
        return self._profile_side_menu_button

    def get_profile_dropdown_menu_button(self):
        self._profile_dropdown_menu_button = Button(self._driver.find_element(By.XPATH, "//a[text() = 'Profile']"))
        return self._profile_dropdown_menu_button

    def get_open_edit_profile_button(self):
        self._open_edit_profile_button = Button(self._driver.find_element(By.XPATH, "//button[text()='Edit profile']"))
        return self._open_edit_profile_button

    def get_profile_page_user_full_name_title(self):
        self._profile_page_user_full_name_title = Label(self._driver.find_element(
            By.XPATH, "//p[@class='profile_name display-4']"))
        return self._profile_page_user_full_name_title

    def get_profile_page_user_country_title(self):
        self._profile_page_user_country_title = Label(self._driver.find_element(
            By.XPATH, "//span[@class='icon icon-country']/following-sibling::span[@class='profile-info_text']"))
        return self._profile_page_user_country_title

    def get_profile_page_user_birthday_title(self):
        self._profile_page_user_birthday_title = Label(self._driver.find_element(
            By.XPATH, "//span[@class='icon icon-birthday']/following-sibling::span[@class='profile-info_text']"))
        return self._profile_page_user_birthday_title

    def get_profile_page_user_photo_img(self):
        self._profile_page_user_photo_img = ImageBox(self._driver.find_element(
            By.XPATH, "//img[@class='profile_photo']"))
        return self._profile_page_user_photo_img

    def get_edit_profile_x_button(self):
        self._edit_profile_x_button = Button(self._driver.find_element(By.XPATH, "//button[@class='close']"))
        return self._edit_profile_x_button

    def get_edit_profile_save_button(self):
        self._edit_profile_save_button = Button(self._driver.find_element(By.XPATH, "//button[text()='Save']"))
        return self._edit_profile_save_button

    def get_edit_profile_name_field(self):
        self._edit_profile_name_field = TextBox(self._driver.find_element(By.ID, "editProfileName"))
        return self._edit_profile_name_field

    def get_edit_profile_last_name_field(self):
        self._edit_profile_last_name_field = TextBox(self._driver.find_element(By.ID, "editProfileLastName"))
        return self._edit_profile_last_name_field

    def get_edit_profile_birthday_field(self):
        self._edit_profile_birthday_field = TextBox(self._driver.find_element(By.ID, "editProfileDateBirth"))
        return self._edit_profile_birthday_field

    def get_edit_profile_country_field(self):
        self._edit_profile_country_field = TextBox(self._driver.find_element(By.ID, "editProfileCountry"))
        return self._edit_profile_country_field

    def get_edit_profile_photo_select_field(self):
        self._edit_profile_photo_select_field = TextBox(self._driver.find_element(By.ID, "editProfilePhoto"))
        return self._edit_profile_photo_select_field

    def get_edit_profile_name_is_required_alert(self):
        self._edit_profile_name_is_required_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Name is required']"))
        return self._edit_profile_name_is_required_alert

    def get_edit_profile_name_not_valid_data_alert(self):
        self._edit_profile_name_not_valid_data_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Name is invalid']"))
        return self._edit_profile_name_not_valid_data_alert

    def get_edit_profile_name_incorrect_data_alert(self):
        self._edit_profile_name_incorrect_data_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Name has to be from 2 to 20 characters long']"))
        return self._edit_profile_name_incorrect_data_alert

    def get_edit_profile_last_name_is_required_alert(self):
        self._edit_profile_last_name_is_required_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Last name is required']"))
        return self._edit_profile_last_name_is_required_alert

    def get_edit_profile_last_name_not_valid_data_alert(self):
        self._edit_profile_last_name_not_valid_data_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Last name is invalid']"))
        return self._edit_profile_last_name_not_valid_data_alert

    def get_edit_profile_last_name_incorrect_data_alert(self):
        self._edit_profile_last_name_incorrect_data_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Last name has to be from 2 to 20 characters long']"))
        return self._edit_profile_last_name_incorrect_data_alert

    def get_user_profile_has_been_updated_alert(self):
        self._user_profile_has_been_updated_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='User profile has been updated']"))
        return self._user_profile_has_been_updated_alert

    def get_edit_profile_country_not_valid_data_alert(self):
        self._edit_profile_country_not_valid_data_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Country is invalid']"))
        return self._edit_profile_country_not_valid_data_alert

    def get_edit_profile_birthday_not_valid_data_alert(self):
        self._edit_profile_birthday_not_valid_data_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Birthday is invalid']"))
        return self._edit_profile_birthday_not_valid_data_alert

    def get_edit_profile_country_incorrect_data_alert(self):
        self._edit_profile_country_incorrect_data_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Country has to be from 2 to 20 characters long']"))
        return self._edit_profile_country_incorrect_data_alert

    def get_edit_profile_birthday_incorrect_data_alert(self):
        self._edit_profile_birthday_incorrect_data_alert = Label(self._driver.find_element(
            By.XPATH, "//p[text()='Birthday is incorrect']"))
        return self._edit_profile_birthday_incorrect_data_alert
