class ChangePasswordModel:
    def __init__(self, old_password, password, repeat_password):
        self.oldPassword = old_password
        self.password = password
        self.repeatPassword = repeat_password
