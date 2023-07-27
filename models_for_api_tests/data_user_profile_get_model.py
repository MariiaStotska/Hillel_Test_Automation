class DataUserProfileGetModel:
    def __init__(self, user_id, photo_file_name, name, last_name):
        self.userId = user_id
        self.photoFilename = photo_file_name
        self.name = name
        self.lastName = last_name

    def __str__(self):
        return self.__dict__
