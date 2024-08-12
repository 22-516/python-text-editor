import hashlib

from encodedtypes import ENCODING_TYPE, EncodeType

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


def decode_from_db_value(db_column, db_value):
    if db_column in ENCODING_TYPE:
        if ENCODING_TYPE[db_column] == EncodeType.HEX:
            return hex_to_tuple_rgb(db_value)
    return db_value

def encode_to_db_value(db_column, db_value):
    if db_column in ENCODING_TYPE:
        if ENCODING_TYPE[db_column] == EncodeType.HEX:
            return tuple_rgb_to_hex(*db_value)
        return db_value