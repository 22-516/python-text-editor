import hashlib
import string
import re

from encodedtypes import ENCODING_TYPE, EncodeType, STRING_MAX_LENGTH, STRING_ALLOW_NUMBERS, STRING_ALLOW_SPECIAL_CHARACTERS

def tuple_rgb_to_hex(r, g, b, _=None):
    # unused var as PyQt rgb values include transparency (unneeded) so we discard
    return f"#{int(round(r)):02x}{int(round(g)):02x}{int(round(b)):02x}"

def hex_to_tuple_rgb(hex_code):
    if not hex_code:
        print("failed to decode from hex")
        return None
    hex_code = hex_code.lstrip('#')
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def hash_password(password):
    return password #testing

def decode_password(hashed_password):#, salt):
    return hashed_password #testing

def check_type_validity(value_type, input_value):
    # valid_state = True
    error_message = None
    if not value_type in ENCODING_TYPE:
        raise KeyError("value_type not in ENCODING_TYPE")
    
    encoding_format = ENCODING_TYPE[value_type]
    
    match encoding_format:
        case EncodeType.HEX:
            # expects a tuple
            if len(input_value) == 0:
                # empty tuple is not allowed, set to None
                # but still valid (save as None)
                input_value = None
        case EncodeType.STR:
            if len(input_value) > STRING_MAX_LENGTH:
                error_message = f"The length must be shorter than {STRING_MAX_LENGTH} characters!"
            if not STRING_ALLOW_SPECIAL_CHARACTERS:
                if any(char in string.punctuation for char in input_value):
                    error_message = "Special characters are not allowed to be used!"
            if not STRING_ALLOW_NUMBERS:
                if re.search(r'[0-9]', input_value):
                    error_message = "Numbers are not allowed to be used!"
        case EncodeType.HASH:
            pass
            
    return error_message, input_value

def decode_from_db_value(db_column, db_value):
    if not db_value:
        return None
    if db_column in ENCODING_TYPE:
        if ENCODING_TYPE[db_column] == EncodeType.HEX:
            return hex_to_tuple_rgb(db_value)
    return db_value

def encode_to_db_value(db_column, db_value):
    if not db_value:
        return None
    if db_column in ENCODING_TYPE:
        if ENCODING_TYPE[db_column] == EncodeType.HEX:
            return tuple_rgb_to_hex(*db_value)
        return db_value