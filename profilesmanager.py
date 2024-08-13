from profilescontroller import *
from usersettingsprofile import UserSettingsProfile

def save_settings_profile_to_db(editor_settings_profile : UserSettingsProfile):
    print(editor_settings_profile)
    
def get_current_user_profile():
    data_list = get_current_and_username_columns()
    
    current_profile = None
    for _, profile in enumerate(data_list):
        #print(profile)
        if profile[0]:
            # integer value 1 == True
            current_profile = profile[1]
            break
    
    return UserSettingsProfile(current_profile)

#print(get_current_user_profile())