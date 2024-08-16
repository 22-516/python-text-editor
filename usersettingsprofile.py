from profilescontroller import get_db_column_names, get_profile_from_username, package_as_zip
from encodedtypes import ENCODING_TYPE
from encodingcontroller import decode_from_db_value

class UserSettingsProfile:
    def __init__(self, profile_name):
        self.user_data = dict.fromkeys(
            get_db_column_names()
        )  # create keys with empty values
        # if profile is saved in database, retrieve data and set values
        if data_list := package_as_zip(get_profile_from_username(profile_name)):
            for _, value_tuple in enumerate(data_list):
                column_name = value_tuple[0]
                value = value_tuple[1]
                if column_name in self.user_data:
                    self.user_data[column_name] = decode_from_db_value(column_name, value)

    def __str__(self):
        return self.user_data.__str__()

    def __getitem__(self, key):
        # if key in ENCODING_TYPE:
        #     print(key, "needs to be decoded", self.user_data[key]) #test
        #     return decode_from_db_value(key, self.user_data[key])
        return self.user_data.__getitem__(key)

        #return self.user_data[key]

    def __setitem__(self, key, value):
        self.user_data[key] = value
        
    def __iter__(self):
        return iter(self.user_data)
        #return self.user_data.__iter__()
