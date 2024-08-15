from enum import Enum

STRING_MAX_LENGTH = 10
STRING_ALLOW_SPECIAL_CHARACTERS = False
STRING_ALLOW_NUMBERS = True
DEFAULT_FONT_SIZE = 12
DEFAULT_FONT_FAMILY = "Arial"
DEFAULT_FONT_SIZE_COLLECTION = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    19,
    21,
    23,
    25,
    28,
    32,
    36,
    40,
    44,
    50,
    62,
    72,
    86,
    100,
]
class EncodeType(Enum):
    HEX = 1
    LIST = 2
    INT = 3
    HASH = 4
    STR = 5
    FONT = 6
    BOOL = 7

ENCODING_TYPE = {
    "editor_background_colour": EncodeType.HEX,
    "editor_colour": EncodeType.HEX,
    "username": EncodeType.STR,
    "default_font": EncodeType.FONT,
    "password": EncodeType.HASH,
    "font_size_collection": EncodeType.LIST,
    "default_font_size": EncodeType.INT,
    "current": EncodeType.BOOL
}
