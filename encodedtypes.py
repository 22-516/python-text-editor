from enum import Enum

class EncodeType(Enum):
    HEX = 1
    LIST = 2

# ENCODED_ITEMS = [
#     "default_font_colour",
#     "default_font_highlight_colour",
#     "editor_background_colour",
#     "editor_colour",
# ]

ENCODING_TYPE = {
    "default_font_colour": EncodeType.HEX,
    "default_font_highlight_colour": EncodeType.HEX,
    "editor_background_colour": EncodeType.HEX,
    "editor_colour": EncodeType.HEX,
}
