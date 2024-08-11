from profilescontroller import *


class EditorSettingsProfile:
    def __init__(self, profile_name):
        self.user_data = dict.fromkeys(
            get_db_column_names()
        )  # create keys with empty values
        if data_list := get_profile_from_username(profile_name):
            for index in enumerate(data_list):
                self.user_data[index] = data_list[index]

    # def __str__(self):
    #     return "a"
