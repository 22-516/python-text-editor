import io
import base64
import os
from pathlib import Path
import tempfile

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_COLOR_INDEX
import docx2txt

from PyQt6.QtCore import *  # temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from encodingcontroller import hex_to_tuple_rgb

# from the svg recognised colour names (https://www.w3.org/TR/SVG11/types.html#ColorKeywords)
# to allow us to look up the nearest colours and correlate them with an enum
COLOURS = (
    (0, 0, 0, WD_COLOR_INDEX.BLACK),
    (255, 0, 0, WD_COLOR_INDEX.BLUE),
    (0, 255, 127, WD_COLOR_INDEX.BRIGHT_GREEN),
    (0, 0, 139, WD_COLOR_INDEX.DARK_BLUE),
    (139, 0, 0, WD_COLOR_INDEX.DARK_RED),
    (218, 165, 32, WD_COLOR_INDEX.DARK_YELLOW),
    (192, 192, 192, WD_COLOR_INDEX.GRAY_25),
    (128, 128, 128, WD_COLOR_INDEX.GRAY_50),
    (0, 128, 0, WD_COLOR_INDEX.GREEN),
    (255, 192, 203, WD_COLOR_INDEX.PINK),
    (255, 0, 0, WD_COLOR_INDEX.RED),
    (0, 128, 128, WD_COLOR_INDEX.TEAL),
    (64, 228, 208, WD_COLOR_INDEX.TURQUOISE),
    (238, 130, 238, WD_COLOR_INDEX.VIOLET),
    (255, 255, 255, WD_COLOR_INDEX.WHITE),
    (255, 255, 0, WD_COLOR_INDEX.YELLOW),
)


def find_nearest_colour(queried_colour):
    """finds the nearest colour to an enum WD_COLOR_INDEX"""
    # we dont need the alpha value (4th index) that is given from QColor
    new_colour = (queried_colour[0], queried_colour[1], queried_colour[2])

    return min(
        COLOURS,
        key=lambda subject: sum(
            (colour - queried) ** 2 for colour, queried in zip(subject, new_colour)
        ),
    )


def apply_formatting(character_format: QTextCharFormat, temp_run):
    """apply formatting to the current run within the paragraph (docx paragraph)"""
    if character_format.font().bold():
        temp_run.bold = True
    if character_format.font().underline():
        temp_run.underline = True
    if character_format.font().italic():
        temp_run.italic = True
    if temp_font_family := character_format.font().family():
        temp_run.font.name = temp_font_family
    if temp_font_size := character_format.font().pointSize():
        temp_run.font.size = Pt(temp_font_size)
    if temp_font_colour := character_format.foreground().color().getRgb():
        temp_run.font.color.rgb = RGBColor(
            temp_font_colour[0], temp_font_colour[1], temp_font_colour[2]
        )
    if temp_font_highlight_colour := character_format.background().color().getRgb():
        temp_run.highlight_color = find_nearest_colour(temp_font_highlight_colour)


def parse_docx_file_to_list(docx_file_path: str):
    """parses the docx file to list format so that the editor can read it"""
    docx_file = Document(docx_file_path)
    file_formatting_list = []

    def docx_colour_to_qcolor(colour):
        return QColor.fromRgb(*colour)

    def qcolor_from_colours(queried_colour: WD_COLOR_INDEX):
        for colour in COLOURS:  # find the enum in the table, then return the rgb values
            if colour[3] == queried_colour:
                return QColor.fromRgb(colour[0], colour[1], colour[2])
        return QColor().fromRgb(0, 0, 0, 0)

    # iterate through the paragraphs
    for paragraph in docx_file.paragraphs:
        for temp_run in paragraph.runs:
            temp_format = QTextCharFormat()
            temp_font = temp_run.font

            formatted_list = None
            current_image_count = 0

            if temp_font.size:
                # this is the only reliable method I found that could detect if an image is present
                # within a run ( when there is an image, font.size is None type )
                # (blame bad documentation!!!)
                temp_format.setFontFamily(temp_font.name)
                temp_format.setFontUnderline(temp_font.underline or False)
                temp_format.setFontItalic(temp_font.italic or False)
                temp_format.setFontWeight(
                    QFont.Weight.Bold if temp_font.bold else QFont.Weight.Normal
                )
                temp_format.setFontPointSize(temp_font.size / 12700)
                temp_format.setBackground(
                    qcolor_from_colours(str(temp_font.highlight_color))
                )
                temp_format.setForeground(
                    docx_colour_to_qcolor(hex_to_tuple_rgb(str(temp_font.color.rgb)))
                )

                formatted_list = (temp_run.text, temp_format)
            else:
                # this is an image format and not text
                image_bytes = None

                current_image_count = current_image_count + 1

                with tempfile.TemporaryDirectory() as temp_directory:
                    # easiest way to get the images ( saved in temp_directory )
                    _ = docx2txt.process(docx_file_path, temp_directory)

                    image_bytes = Path(
                        os.path.join(temp_directory, f"image{current_image_count}.png")
                    ).read_bytes()

                    binary = base64.b64encode(image_bytes)
                    html_bin = '<img src= "data:image/*;base64,{}" max-width=100% max-height=100%></img>'.format(
                        str(binary, "utf-8")
                    )
                formatted_list = html_bin
            file_formatting_list.append(formatted_list)
    return file_formatting_list


def parse_editor_document_to_docx(editor_document: QTextDocument):
    """parses the editor to a docx file so the editor can save it"""
    doc = Document()
    paragraph = doc.add_paragraph()

    cursor = QTextCursor(editor_document)
    cursor.movePosition(QTextCursor.MoveOperation.Start)

    # iterate through the cursor selected items
    while not cursor.atEnd():
        cursor.clearSelection()
        cursor.movePosition(
            QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor
        )
        cursor_format = cursor.charFormat()
        if cursor_format.isImageFormat():
            url = QUrl(cursor.charFormat().toImageFormat().name())
            image = editor_document.resource(
                QTextDocument.ResourceType.ImageResource, url
            )
            image = QImage(image)
            buffer = QBuffer()
            buffer.open(QBuffer.OpenModeFlag.ReadWrite)
            image.save(buffer, "PNG")
            # save the image to a buffer first, then reading from the buffer as bytes
            # because we need the raw image data
            temp_run = paragraph.add_run()
            temp_run.add_picture(io.BytesIO(buffer.data()))
        elif cursor_format.isCharFormat():
            selected_text = cursor.selectedText()  # this returns newlines as unicode
            if (
                "\u2029" in selected_text
            ):  # convert the page break separator (unicode) back to newline character
                selected_text = "\n"  # replace with newline character
            temp_run = paragraph.add_run(selected_text)
            apply_formatting(cursor_format, temp_run)

    return doc
