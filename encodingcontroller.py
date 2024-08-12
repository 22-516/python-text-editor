ENCODED_ITEMS = [
    "default_font_colour",
    "default_font_highlight_colour",
    "editor_background_colour",
    "editor_colour",
]

ENCODING_TYPE = {
    "default_font_colour": "hex",
    "default_font_highlight_colour": "hex",
    "editor_background_colour": "hex",
    "editor_colour": "hex",
}

import hashlib

def tuple_rgb_to_hex(r, g, b):
    return f"#{int(round(r)):02x}{int(round(g)):02x}{int(round(b)):02x}"

def hex_to_tuple_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def hash_password(password):
    return password #testing

def decode_password(hashed_password):#, salt):
    return hashed_password #testing

def decode_from_db(db_column, db_value):
    if db_column in ENCODED_ITEMS:
        if ENCODING_TYPE[db_column] == "hex":
            return hex_to_tuple_rgb(db_value)
    return db_value

def encode_to_db(db_column, db_value):
    if db_column in ENCODED_ITEMS:
        if ENCODING_TYPE[db_column] == "hex":
            return tuple_rgb_to_hex(*db_value)