import sqlite3
import os
from filescontroller import get_data_directory_path

def initialise_database():
    conn = sqlite3.connect(os.path.join(get_data_directory_path(), "userprofiles.db"))

    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS profiles
                (
                    username text, 
                    password_hash text, 
                    default_font text, 
                    default_font_size real, 
                    price real)
                """)
    
    cursor.execute("""INSERT INTO profiles
                (username, password_hash)
                VALUES 
                ("hawk", "superhawk")
                """)
    conn.commit()
    
    conn.close()

def get_value_from_profile(profile_name, queried_value):
    conn = sqlite3.connect(os.path.join(get_data_directory_path(), "userprofiles.db"))

    cursor = conn.cursor()

    query = f"""SELECT ({queried_value}) FROM profiles WHERE username=?"""
    cursor.execute(query, (profile_name,))

    data_list = cursor.fetchone()
    conn.close()

    if not data_list:
        return None

    value = data_list[0]
    return value

def get_profile_from_username(profile_name):
    conn = sqlite3.connect(os.path.join(get_data_directory_path(), "userprofiles.db"))

    cursor = conn.cursor()

    query = """SELECT * FROM profiles WHERE username=?"""
    cursor.execute(query, (profile_name,))

    data_list = cursor.fetchone()
    conn.close()

    return data_list

def get_db_column_names():
    conn = sqlite3.connect(os.path.join(get_data_directory_path(), "userprofiles.db"))

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles")

    column_names = [description[0] for description in cursor.description]
    
    return column_names

def package_as_zip(data_list):
    column_names = get_db_column_names()

    packaged = zip(column_names, data_list)
    return packaged

initialise_database()
package_as_zip(get_profile_from_username("hawk"))
