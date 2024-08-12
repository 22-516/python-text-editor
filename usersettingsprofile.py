from profilescontroller import get_db_column_names, get_profile_from_username, package_as_zip
from encodedtypes import ENCODING_TYPE
from encodingcontroller import decode_from_db_value

# ENCODED_ITEMS = [
#     "default_font_colour",
#     "default_font_highlight_colour",
#     "editor_background_colour",
#     "editor_colour",
# ]

class UserSettingsProfile:
    def __init__(self, profile_name):
        self.user_data = dict.fromkeys(
            get_db_column_names()
        )  # create keys with empty values
        # if profile is saved in database, retrieve data and set values
        if data_list := package_as_zip(get_profile_from_username(profile_name)):
            # print(data_list)
            # print(self.user_data)
            for _, value_tuple in enumerate(data_list):
                column_name = value_tuple[0]
                value = value_tuple[1]
                # print(column_name, value, "kwfefkjwekfwefjkwe")
                if column_name in self.user_data:
                    self.user_data[column_name] = value
                    
            # print("jkakjjkfjkwjkfwajkfwe")
            # print(self.user_data)

    def __str__(self):
        return self.user_data.__str__()

    def __getitem__(self, key):
        if key in ENCODING_TYPE:
            print(key, "needs to be decoded", self.user_data[key]) #test
            return decode_from_db_value(key, self.user_data[key])
        
        return self.user_data[key]

    def __setitem__(self, key, value):
        self.user_data[key] = value
        
    def __iter__(self):
        return iter(self.user_data)
        #return self.user_data.__iter__()
