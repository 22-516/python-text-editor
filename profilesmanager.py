from profilescontroller import *
from usersettingsprofile import UserSettingsProfile
from encodingcontroller import encode_to_db_value


def save_settings_profile_to_db(editor_settings_profile: UserSettingsProfile):
    """save the user settings into the db locally"""
    all_profiles = get_all_entries()

    def username_exists(input_username):
        if not all_profiles:
            return False
        for _, profile in enumerate(all_profiles):
            if profile[1] == input_username:
                return True
        return False

    if not username_exists(editor_settings_profile["username"]):
        add_new_profile(editor_settings_profile["username"])

    for _, profile_setting in enumerate(editor_settings_profile):
        # print(profile_setting, editor_settings_profile[profile_setting])
        setting_name = profile_setting
        setting_value = editor_settings_profile[profile_setting]

        encoded_value = encode_to_db_value(setting_name, setting_value)

        save_value_to_profile(
            editor_settings_profile["username"], setting_name, encoded_value
        )

    set_profile_as_current(editor_settings_profile["username"])


def set_profile_as_current(profile_name):
    """save the selected proifle name as the current one so its loaded by default on editor launch"""
    all_profiles = get_all_entries()

    if not all_profiles:
        return False
    for _, profile in enumerate(all_profiles):
        save_value_to_profile(profile[1], "current", 0) # set current value of every other profile to 0 (false)
    save_value_to_profile(profile_name, "current", 1) # set own to True (1)


def get_current_user_profile():
    """gets the settings with the current value ticked, for default setting"""
    data_list = get_current_and_username_columns()

    if not data_list: # no data exists, create default table
        return UserSettingsProfile(None)

    current_profile = None
    for _, profile in enumerate(data_list):
        # if the first column is 1, it means the current profile
        if profile[0]:
            # integer value 1 == True
            current_profile = profile[1]
            break

    return UserSettingsProfile(current_profile)
