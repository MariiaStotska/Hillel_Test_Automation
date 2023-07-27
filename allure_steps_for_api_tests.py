import allure
from models_for_api_tests.register_post_model import RegisterPostModel
from models_for_api_tests.signin_post_model import SigninPostModel
from models_for_api_tests.reset_password_model import ResetPasswordModel
from models_for_api_tests.data_user_profile_get_model import DataUserProfileGetModel
from models_for_api_tests.update_user_profile_model import UpdateUserProfileModel
from models_for_api_tests.change_email_model import ChangeEmailModel
from models_for_api_tests.change_password_model import ChangePasswordModel
from models_for_api_tests.data_user_settings_get_model import DataUserSettingsGetModel
from models_for_api_tests.edit_user_settings_model import EditUsersSettingsModel


class AllureSteps:
    @allure.step("Data user profile")
    def data_user_profile(self, user_id, photo_file_name, name, last_name):
        return DataUserProfileGetModel(user_id, photo_file_name, name, last_name)

    @allure.step("Data to update user profile")
    def update_user_profile_data(self, photo, name, last_name, date_birth, country):
        return UpdateUserProfileModel(photo, name, last_name, date_birth, country)

    @allure.step("Data to reset password")
    def user_data_reset_password(self, email):
        return ResetPasswordModel(email)

    @allure.step('Data for registering user')
    def user_data_create(self, name, last_name, email, password, repeat_password):
        return RegisterPostModel(name, last_name, email, password, repeat_password)

    @allure.step('Data to signin')
    def user_data_signin(self, email, password, remember):
        return SigninPostModel(email, password, remember)

    @allure.step('Data to change password')
    def user_data_change_password(self, old_password, password, repeat_password):
        return ChangePasswordModel(old_password, password, repeat_password)

    @allure.step('Get user settings data')
    def get_user_settings_data(self, currency, distance_units):
        return DataUserSettingsGetModel(currency, distance_units)

    @allure.step('Edit user settings data')
    def edit_user_settings_data(self, currency, distance_units):
        return EditUsersSettingsModel(currency, distance_units)

    @allure.step("Data to change email")
    def user_change_email_data(self, email, password):
        return ChangeEmailModel(email, password)
