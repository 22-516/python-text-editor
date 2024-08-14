from enum import Enum

STRING_MAX_LENGTH = 10
STRING_ALLOW_SPECIAL_CHARACTERS = False
STRING_ALLOW_NUMBERS = True

class EncodeType(Enum):
    HEX = 1
    LIST = 2
    INT = 3
    HASH = 4
    STR = 5
    FONT = 6
    BOOL = 7

ENCODING_TYPE = {
    "default_font_colour": EncodeType.HEX,
    "default_font_highlight_colour": EncodeType.HEX,
    "editor_background_colour": EncodeType.HEX,
    "editor_colour": EncodeType.HEX,
    "username": EncodeType.STR,
    "default_font": EncodeType.FONT,
    "password": EncodeType.HASH,
    "font_size_collection": EncodeType.LIST,
    "default_font_size": EncodeType.INT,
    "current": EncodeType.BOOL
}
