import pytest
import requests
from allure_steps_for_api_tests import AllureSteps


class TestApiChecks:

    allure_steps = AllureSteps()
    sign_in_data = allure_steps.user_data_signin("fedorchuck_maya@gmail.com", "Maya1997ML", "False")
    user_id = None

    def setup_class(self):
        self.session = requests.session()
        self.register_user_data = self.allure_steps.user_data_create("Maya", "Fedorchuk", "fedorchuck_maya@gmail.com",
                                                                     "Maya1997ML", "Maya1997ML")
        self.session.post("https://qauto.forstudy.space/api/auth/signup", json=self.register_user_data.__dict__)

    def setup_method(self):
        self.session.post("https://qauto.forstudy.space/api/auth/signin", json=TestApiChecks.sign_in_data.__dict__)

    def test_check_successful_registration_user(self):
        self.session.delete("https://qauto.forstudy.space/api/users")
        data_for_register_user = self.allure_steps.user_data_create("Maya", "Fedorchuk", "fedorchuck_maya@gmail.com",
                                                                    "Maya1997ML", "Maya1997ML")
        registered_user = self.session.post("https://qauto.forstudy.space/api/auth/signup",
                                            json=data_for_register_user.__dict__)
        assert registered_user.json()["status"] == "ok"

    def test_check_registration_with_registered_user(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        data_for_register_user = self.allure_steps.user_data_create("Maya", "Fedorchuk", "fedorchuck_maya@gmail.com",
                                                                    "Maya1997ML", "Maya1997ML")
        registered_user = self.session.post("https://qauto.forstudy.space/api/auth/signup",
                                            json=data_for_register_user.__dict__)
        assert registered_user.json()["status"] == "error"
        assert registered_user.json()["message"] == "User already exists"

    def test_check_registration_with_no_full_data(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        try:
            data_for_register_user = self.allure_steps.user_data_create(name="Maya",
                                                                        email="fedorchuck_maya@gmail.com",
                                                                        password="Maya1997ML",
                                                                        repeat_password="Maya1997ML")
            self.session.post("https://qauto.forstudy.space/api/auth/signup", json=data_for_register_user.__dict__)
            assert False
        except TypeError:
            assert True

    @pytest.mark.parametrize("name, last_name, email, password, repeat_password, expected_message", [
        ("E", "Fedorchuk", "fedorchuck_maya@gmail.com", "Maya1997ML", "Maya1997ML",
         "Name has to be from 2 to 20 characters long"),
        ("Maya", "L@", "fedorchuck_maya@gmail.com", "Maya1997ML", "Maya1997ML", "Last Name is invalid"),
        ("Maya", "Fedorchuck", "@gmail.com", "Maya1997ML", "Maya1997ML", "Email is incorrect"),
        ("Maya", "Fedorchuk", "fedorchuck_maya@gmail.com", "MayaMaya", "MayaMaya",
         "Password has to be from 8 to 15 characters long and contain at least one integer, one capital, "
         "and one small letter"),
        ("Maya", "Fedorchuck", "fedorchuck_maya@gmail.com", "Maya1997ML", "Maya1997MLN", "Passwords do not match")
    ])
    def test_registration_with_incorrect_data(self, name, last_name, email, password, repeat_password,
                                              expected_message):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        data_for_register_user = self.allure_steps.user_data_create(name, last_name, email, password, repeat_password)
        registered_user = self.session.post("https://qauto.forstudy.space/api/auth/signup",
                                            json=data_for_register_user.__dict__)
        assert registered_user.json()['status'] == 'error'
        assert registered_user.json()["message"] == expected_message

    def test_successful_sign_in_with_false_remember(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        sign_in_user = self.session.post("https://qauto.forstudy.space/api/auth/signin",
                                         json=TestApiChecks.sign_in_data.__dict__)
        assert sign_in_user.json()['status'] == 'ok'
        assert sign_in_user.json()['data']['distanceUnits'] == 'km'
        assert sign_in_user.json()['data']['currency'] == 'usd'

    def test_signin_with_wrong_email(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        sign_in_data = self.allure_steps.user_data_signin("fedorchuck_ma@gmail.com", "Maya1997ML", "False")
        sign_in_user = self.session.post("https://qauto.forstudy.space/api/auth/signin", json=sign_in_data.__dict__)
        assert sign_in_user.json()['status'] == 'error'
        assert sign_in_user.json()['message'] == 'Wrong email or password'

    def test_signin_without_password(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        sign_in_data = self.allure_steps.user_data_signin("fedorchuck_maya@gmail.com", "", "False")
        sign_in_user = self.session.post("https://qauto.forstudy.space/api/auth/signin", json=sign_in_data.__dict__)
        assert sign_in_user.json()['status'] == 'error'
        assert sign_in_user.json()['message'] == '"password" is not allowed to be empty'    #

    def test_signin_without_email(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        sign_in_data = self.allure_steps.user_data_signin("", "Maya1997ML", "False")
        sign_in_user = self.session.post("https://qauto.forstudy.space/api/auth/signin", json=sign_in_data.__dict__)
        assert sign_in_user.json()['status'] == 'error'
        assert sign_in_user.json()['message'] == '"email" is not allowed to be empty'

    def test_signin_with_invalid_email(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        sign_in_data = self.allure_steps.user_data_signin("!!", "Maya1997ML", "False")
        sign_in_user = self.session.post("https://qauto.forstudy.space/api/auth/signin", json=sign_in_data.__dict__)
        assert sign_in_user.json()['status'] == 'error'
        assert sign_in_user.json()['message'] == 'Email is invalid'

    def test_successful_logout(self):
        logout = self.session.get("https://qauto.forstudy.space/api/auth/logout")
        assert logout.json()['status'] == 'ok'

    def test_successful_restore_password(self):
        reset_password_data = self.allure_steps.user_data_reset_password('fedorchuck_maya@gmail.com')
        reset_password = self.session.post('https://qauto.forstudy.space/api/auth/resetPassword',
                                           json=reset_password_data.__dict__)
        assert reset_password.json()['status'] == 'ok'

    def test_restore_password_without_email(self):
        reset_password_data = self.allure_steps.user_data_reset_password('')
        reset_password = self.session.post('https://qauto.forstudy.space/api/auth/resetPassword',
                                           json=reset_password_data.__dict__)
        assert reset_password.json()['status'] == 'error'
        assert reset_password.json()['message'] == '"email" is not allowed to be empty'

    def test_restore_password_with_invalid_email(self):
        reset_password_data = self.allure_steps.user_data_reset_password('fedorchuck_maya@gm@ail.com')
        reset_password = self.session.post('https://qauto.forstudy.space/api/auth/resetPassword',
                                           json=reset_password_data.__dict__)
        assert reset_password.json()['status'] == 'error'
        assert reset_password.json()['message'] == 'Email is incorrect'

    def test_get_user_profile(self):
        result = self.session.get(url="https://qauto.forstudy.space/api/users/profile")
        TestApiChecks.user_id = result.json()['data']['userId']
        data = self.allure_steps.data_user_profile(TestApiChecks.user_id, 'default-user.png',
                                                   self.register_user_data.name, self.register_user_data.lastName)
        assert result.json()["data"] == data.__dict__
        assert result.json()["status"] == 'ok'

    def test_get_profile_data_when_user_is_not_logged_in(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        result = self.session.get(url="https://qauto.forstudy.space/api/users/profile")
        assert result.json()["message"] == 'Not authenticated'
        assert result.json()["status"] == 'error'

    def test_edit_user_profile_user_is_not_authenticated(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        user_edit_data = self.allure_steps.update_user_profile_data('default-user.png', "Masha", 'Stotska', 'USA',
                                                                    '2020-03-17T15:21:05.000Z')
        user_to_edit = self.session.put(url="https://qauto.forstudy.space/api/users/profile",
                                        json=user_edit_data.__dict__)
        assert user_to_edit.json()["message"] == 'Not authenticated'
        assert user_to_edit.json()["status"] == 'error'

    def test_edit_user_profile(self):
        user_to_update = self.allure_steps.update_user_profile_data(photo="default-user.png", name="Olya",
                                                                    last_name="Dou", country="USA",
                                                                    date_birth="2021-03-17T15:21:05.000Z")

        result = self.session.put("https://qauto.forstudy.space/api/users/profile", json=user_to_update.__dict__)
        assert result.json()['status'] == 'ok'
        assert result.json()['data']['name'] == 'Olya'
        assert result.json()['data']['country'] == 'USA'
        self.session.delete("https://qauto.forstudy.space/api/users")
        self.register_user_data = self.allure_steps.user_data_create("Maya", "Fedorchuk", "fedorchuck_maya@gmail.com",
                                                                     "Maya1997ML", "Maya1997ML")
        self.session.post("https://qauto.forstudy.space/api/auth/signup", json=self.register_user_data.__dict__)
        self.session.post("https://qauto.forstudy.space/api/auth/signin", json=TestApiChecks.sign_in_data.__dict__)

    def test_successful_change_email(self):
        new_email = self.allure_steps.user_change_email_data("test2002@test.com", "Maya1997ML")
        changed_email = self.session.put(url='https://qauto.forstudy.space/api/users/email', json=new_email.__dict__)
        assert changed_email.json()['status'] == 'ok'
        self.session.delete("https://qauto.forstudy.space/api/users")
        self.register_user_data = self.allure_steps.user_data_create("Maya", "Fedorchuk", "fedorchuck_maya@gmail.com",
                                                                     "Maya1997ML", "Maya1997ML")
        self.session.post("https://qauto.forstudy.space/api/auth/signup", json=self.register_user_data.__dict__)
        self.session.post("https://qauto.forstudy.space/api/auth/signin", json=TestApiChecks.sign_in_data.__dict__)

    def test_change_email_with_current_email(self):
        new_email = self.allure_steps.user_change_email_data("fedorchuck_maya@gmail.com", "Maya1997ML")
        changed_email = self.session.put(url='https://qauto.forstudy.space/api/users/email', json=new_email.__dict__)
        assert changed_email.json()['status'] == 'error'
        assert changed_email.json()['message'] == 'The email should not be the same'

    def test_change_email_with_invalid_email(self):
        new_email = self.allure_steps.user_change_email_data("test !1999@test.com", "Maya1997ML")
        changed_email = self.session.put(url='https://qauto.forstudy.space/api/users/email',
                                         json=new_email.__dict__)
        assert changed_email.json()['status'] == 'error'
        assert changed_email.json()['message'] == 'Email is incorrect'

    def test_change_email_with_wrong_password(self):
        new_email = self.allure_steps.user_change_email_data("test1999@test.com", "Maya__1997ML")
        changed_email = self.session.put(url='https://qauto.forstudy.space/api/users/email',
                                         json=new_email.__dict__)
        assert changed_email.json()['status'] == 'error'
        assert changed_email.json()['message'] == 'Wrong password'

    def test_change_email_empty_fields(self):
        new_email = self.allure_steps.user_change_email_data("", "")
        changed_email = self.session.put(url='https://qauto.forstudy.space/api/users/email',
                                         json=new_email.__dict__)
        assert changed_email.json()['status'] == 'error'
        assert changed_email.json()['message'] == '"email" is not allowed to be empty'

    def test_change_email_user_is_not_logged_in(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        new_email = self.allure_steps.user_change_email_data("test2002@test.com", "Maya1997ML")
        changed_email = self.session.put(url='https://qauto.forstudy.space/api/users/email',
                                         json=new_email.__dict__)
        assert changed_email.json()['status'] == 'error'
        assert changed_email.json()['message'] == 'Not authenticated'

    def test_successful_change_password(self):
        change_password_data = self.allure_steps.user_data_change_password("Maya1997ML", "Lunych1997L", "Lunych1997L")
        changed_password = self.session.put(url='https://qauto.forstudy.space/api/users/password',
                                            json=change_password_data.__dict__)
        assert changed_password.json()['status'] == 'ok'
        self.session.delete("https://qauto.forstudy.space/api/users")
        self.register_user_data = self.allure_steps.user_data_create("Maya", "Fedorchuk", "fedorchuck_maya@gmail.com",
                                                                     "Maya1997ML", "Maya1997ML")
        self.session.post("https://qauto.forstudy.space/api/auth/signup", json=self.register_user_data.__dict__)
        self.session.post("https://qauto.forstudy.space/api/auth/signin", json=TestApiChecks.sign_in_data.__dict__)

    def test_change_password_with_old_password(self):
        change_password_data = self.allure_steps.user_data_change_password("Maya1997ML", "Maya1997ML", "Maya1997ML")
        changed_password = self.session.put(url='https://qauto.forstudy.space/api/users/password',
                                            json=change_password_data.__dict__)
        assert changed_password.json()['status'] == 'error'
        assert changed_password.json()['message'] == 'New password should not be the same'

    def test_change_password_with_wrong_current_password(self):
        change_password_data = self.allure_steps.user_data_change_password("Maya 1997ML", "Lunych1997L", "Lunych1997L")
        changed_password = self.session.put(url='https://qauto.forstudy.space/api/users/password',
                                            json=change_password_data.__dict__)
        assert changed_password.json()['status'] == 'error'
        assert changed_password.json()['message'] == 'Wrong password'

    def test_change_password_passwords_do_not_match(self):
        change_password_data = self.allure_steps.user_data_change_password("Maya1997ML", "Lunych1997L", "Lunych1998L")
        changed_password = self.session.put(url='https://qauto.forstudy.space/api/users/password',
                                            json=change_password_data.__dict__)
        assert changed_password.json()['status'] == 'error'
        assert changed_password.json()['message'] == 'Passwords do not match'

    def test_change_password_with_empty_password_field(self):
        change_password_data = self.allure_steps.user_data_change_password("Maya1997ML", "", "Lunych1997L")
        changed_password = self.session.put(url='https://qauto.forstudy.space/api/users/password',
                                            json=change_password_data.__dict__)
        assert changed_password.json()['status'] == 'error'
        assert changed_password.json()['message'] == '"password" is not allowed to be empty'

    def test_change_password_with_empty_old_password_field(self):
        change_password_data = self.allure_steps.user_data_change_password("", "Lunych1997L", "Lunych1997L")
        changed_password = self.session.put(url='https://qauto.forstudy.space/api/users/password',
                                            json=change_password_data.__dict__)
        assert changed_password.json()['status'] == 'error'
        assert changed_password.json()['message'] == '"oldPassword" is not allowed to be empty'

    def test_change_password_with_empty_reentry_password_field(self):
        change_password_data = self.allure_steps.user_data_change_password("Maya1997ML", "Lunych1997L", "")
        changed_password = self.session.put(url='https://qauto.forstudy.space/api/users/password',
                                            json=change_password_data.__dict__)
        assert changed_password.json()['status'] == 'error'
        assert changed_password.json()['message'] == '"repeatPassword" is not allowed to be empty'

    def test_change_password_with_incorrect_data(self):
        change_password_data = self.allure_steps.user_data_change_password("Maya1997ML", "5", "5")
        changed_password = self.session.put(url='https://qauto.forstudy.space/api/users/password',
                                            json=change_password_data.__dict__)
        assert changed_password.json()['status'] == 'error'
        assert changed_password.json()['message'] == 'Password has to be from 8 to 15 characters long and contain' \
                                                     ' at least one integer, one capital and one small letter'

    def test_change_password_user_is_not_logged_in(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        change_password_data = self.allure_steps.user_data_change_password("Maya1997ML", "Lunych1999L", "Lunych1999L")
        changed_password = self.session.put(url='https://qauto.forstudy.space/api/users/password',
                                            json=change_password_data.__dict__)
        assert changed_password.json()['status'] == 'error'
        assert changed_password.json()['message'] == 'Not authenticated'

    def test_gets_authenticated_user_settings_data(self):
        get_user_settings = self.session.get(url='https://qauto.forstudy.space/api/users/settings')
        data = self.allure_steps.get_user_settings_data('usd', 'km')
        assert get_user_settings.json()['data'] == data.__dict__
        assert get_user_settings.json()["status"] == 'ok'

    def test_get_settings_user_not_authenticated(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        get_user_settings = self.session.get(url='https://qauto.forstudy.space/api/users/settings')
        assert get_user_settings.json()["status"] == 'error'
        assert get_user_settings.json()["message"] == 'Not authenticated'

    def test_successful_change_data_in_user_settings(self):
        data_to_change = self.allure_steps.edit_user_settings_data('pln', 'ml')
        change_user_settings = self.session.put(url='https://qauto.forstudy.space/api/users/settings',
                                                json=data_to_change.__dict__)
        assert change_user_settings.json()['status'] == 'ok'
        assert change_user_settings.json()['data']['currency'] == 'pln'
        assert change_user_settings.json()['data']['distanceUnits'] == 'ml'

        self.session.delete("https://qauto.forstudy.space/api/users")
        self.register_user_data = self.allure_steps.user_data_create("Maya", "Fedorchuk", "fedorchuck_maya@gmail.com",
                                                                     "Maya1997ML", "Maya1997ML")
        self.session.post("https://qauto.forstudy.space/api/auth/signup", json=self.register_user_data.__dict__)
        self.session.post("https://qauto.forstudy.space/api/auth/signin", json=TestApiChecks.sign_in_data.__dict__)

    def test_change_data_in_user_settings_incorrect_distance_units(self):
        data_to_change = self.allure_steps.edit_user_settings_data('pln', '#')
        change_user_settings = self.session.put(url='https://qauto.forstudy.space/api/users/settings',
                                                json=data_to_change.__dict__)
        assert change_user_settings.json()['status'] == 'error'
        assert change_user_settings.json()['message'] == 'Distance units not found'

    def test_change_data_in_user_settings_incorrect_currency(self):
        data_to_change = self.allure_steps.edit_user_settings_data('mex', 'km')
        change_user_settings = self.session.put(url='https://qauto.forstudy.space/api/users/settings',
                                                json=data_to_change.__dict__)
        assert change_user_settings.json()['status'] == 'error'
        assert change_user_settings.json()['message'] == 'Currency not found'

    def test_delete_user(self):
        delete_user = self.session.delete("https://qauto.forstudy.space/api/users")
        assert delete_user.json()['status'] == 'ok'
        self.register_user_data = self.allure_steps.user_data_create("Maya", "Fedorchuk", "fedorchuck_maya@gmail.com",
                                                                     "Maya1997ML", "Maya1997ML")
        self.session.post("https://qauto.forstudy.space/api/auth/signup", json=self.register_user_data.__dict__)
        self.session.post("https://qauto.forstudy.space/api/auth/signin", json=TestApiChecks.sign_in_data.__dict__)

    def test_delete_not_authenticated_user(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")
        delete_user = self.session.delete("https://qauto.forstudy.space/api/users")
        assert delete_user.json()['status'] == 'error'
        assert delete_user.json()['message'] == 'Not authenticated'

    def teardown_method(self):
        self.session.get("https://qauto.forstudy.space/api/auth/logout")

    def teardown_class(self):
        self.session.post("https://qauto.forstudy.space/api/auth/signin", json=TestApiChecks.sign_in_data.__dict__)
        self.session.delete("https://qauto.forstudy.space/api/users")
