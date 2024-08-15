import hashlib
import string
import re

from PyQt6.QtGui import QFont, QFontInfo

from encodedtypes import (
    ENCODING_TYPE,
    EncodeType,
    STRING_MAX_LENGTH,
    STRING_ALLOW_NUMBERS,
    STRING_ALLOW_SPECIAL_CHARACTERS,
    PASSWORD_CAPITAL_LETTER_AMOUNT,
    PASSWORD_MAXIMUM_CHARACTERS,
    PASSWORD_MUST_CONTAIN_NUMBERS,
    PASSWORD_MINIMUM_CHARACTERS,
    PASSWORD_MUST_CONTAIN_CAPITAL_LETTER,
    PASSWORD_MUST_CONTAIN_SPECIAL_CHARACTERS,
    PASSWORD_NUMBER_AMOUNT,
    PASSWORD_SPECIAL_CHARACTER_AMOUNT,
)


def tuple_rgb_to_hex(r, g, b, _=None):
    # unused var as PyQt rgb values include transparency (unneeded) so we discard
    return f"#{int(round(r)):02x}{int(round(g)):02x}{int(round(b)):02x}"


def hex_to_tuple_rgb(hex_code):
    if not hex_code:
        print("failed to decode from hex")
        return None
    hex_code = hex_code.lstrip("#")
    rgb = tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))
    return rgb


def list_encode_to_string(input_list: list):
    if not input_list:
        return None
    return "/".join(map(str, input_list))


def string_decode_to_list(input_string: str):
    if not input_string:
        return None
    return input_string.split("/")


def qfont_to_string(input_font: QFont):
    return QFontInfo(input_font).family()


def string_to_qfont(input_string: str):
    return QFont(input_string)


def hash_password(password):
    return password  # testing


def decode_password(hashed_password):  # , salt):
    return hashed_password  # testing


def check_type_validity(value_type, input_value):
    if not value_type in ENCODING_TYPE:
        raise KeyError("value_type not in ENCODING_TYPE")

    error_message = ""

    def append_error_message(new_line):
        pass

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
                append_error_message(
                    f"The length must be shorter than {STRING_MAX_LENGTH} characters!"
                )
            if not STRING_ALLOW_SPECIAL_CHARACTERS:
                if any(char in string.punctuation for char in input_value):
                    append_error_message(
                        "Special characters are not allowed to be used!"
                    )
            if not STRING_ALLOW_NUMBERS:
                if re.search(r"[0-9]", input_value):
                    append_error_message("Numbers are not allowed to be used!")
        case EncodeType.HASH:
            if len(input_value) > PASSWORD_MAXIMUM_CHARACTERS:
                append_error_message(
                    f"The password length must be shorter than {PASSWORD_MAXIMUM_CHARACTERS} characters!"
                )
            if len(input_value) < PASSWORD_MINIMUM_CHARACTERS:
                append_error_message(
                    f"The password length must be longer than {PASSWORD_MINIMUM_CHARACTERS} characters!"
                )
            if PASSWORD_MUST_CONTAIN_CAPITAL_LETTER:
                if (
                    len(re.findall(r"[A-Z]", input_value))
                    < PASSWORD_CAPITAL_LETTER_AMOUNT
                ):
                    append_error_message(
                        f"The password must contain {PASSWORD_CAPITAL_LETTER_AMOUNT} capital letters!"
                    )
            if PASSWORD_MUST_CONTAIN_SPECIAL_CHARACTERS:
                if (
                    len(re.findall(r"[\w]+", input_value))
                    < PASSWORD_SPECIAL_CHARACTER_AMOUNT
                ):
                    append_error_message(
                        f"The password must contain {PASSWORD_SPECIAL_CHARACTER_AMOUNT} special characters! e.g (!@#$%^&*-+)"
                    )
            if PASSWORD_MUST_CONTAIN_NUMBERS:
                if len(re.findall(r"[0-9]", input_value)) < PASSWORD_NUMBER_AMOUNT:
                    append_error_message(
                        f"The password must contain {PASSWORD_NUMBER_AMOUNT} numbers!"
                    )
        case EncodeType.LIST:
            for _, font_size in enumerate(input_value):
                if not font_size.replace(".", "", 1).isdigit():
                    append_error_message("Only numbers are allowed to be used!")
                else:
                    if float(font_size) < 0:
                        append_error_message(
                            "Only positive numbers are allowed to be used!"
                        )
        case EncodeType.INT:
            if not str(input_value).replace(".", "", 1).isdigit():
                append_error_message("Only numbers are allowed to be used!")
            else:
                if float(input_value) < 0:
                    append_error_message(
                        "Only positive numbers are allowed to be used!"
                    )

    if not error_message:
        error_message = None

    return error_message, input_value


def decode_from_db_value(db_column, db_value):
    if not db_value:
        return None
    if db_column in ENCODING_TYPE:
        match ENCODING_TYPE[db_column]:
            case EncodeType.HEX:
                return hex_to_tuple_rgb(db_value)
            case EncodeType.LIST:
                return string_decode_to_list(db_value)
            case EncodeType.FONT:
                return string_to_qfont(db_value)
            case _:
                print("no encoding", db_column, db_value)
                return db_value


def encode_to_db_value(db_column, db_value):
    if not db_value:
        return None
    if db_column in ENCODING_TYPE:
        match ENCODING_TYPE[db_column]:
            case EncodeType.HEX:
                return tuple_rgb_to_hex(*db_value)
            case EncodeType.LIST:
                return list_encode_to_string(db_value)
            case EncodeType.FONT:
                return qfont_to_string(db_value)
            case _:
                print("no encoding", db_column, db_value)
                return db_value
