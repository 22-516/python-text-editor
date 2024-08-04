from docx import Document
from docx.shared import Inches, Pt
import mammoth
import io

from PyQt6.QtCore import *  # temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

def apply_formatting(character_format : QTextCharFormat, temp_run):
    if character_format.font().bold():
        temp_run.bold = True
    if character_format.font().underline():
        temp_run.underline = True
    if character_format.font().italic():
        temp_run.italic = True
    if temp_font_family := character_format.font().family():
        temp_run.font.name = temp_font_family
    if temp_font_size :=character_format.font().pointSize():
        temp_run.font.size = Pt(temp_font_size)

def parse_docx_file_to_html(docx_file_path: str):
    with open(docx_file_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value
        messages = result.messages
        # print(messages)
        # print(html)
        return html

def parse_editor_document_to_docx(editor_document: QTextDocument):
    doc = Document()
    paragraph = doc.add_paragraph()

    cursor = QTextCursor(editor_document)
    cursor.movePosition(QTextCursor.MoveOperation.Start)

    while not cursor.atEnd():
        cursor.clearSelection()
        cursor.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor)
        cursor_format = cursor.charFormat()
        if cursor_format.isImageFormat():
            url = QUrl(cursor.charFormat().toImageFormat().name())
            image = editor_document.resource(QTextDocument.ResourceType.ImageResource, url)
            image = QImage(image)
            buffer = QBuffer()
            buffer.open(QBuffer.OpenModeFlag.ReadWrite)
            image.save(buffer, "PNG")

            temp_run = paragraph.add_run()
            temp_run.add_picture(io.BytesIO(buffer.data()))
        elif cursor_format.isCharFormat():
            selected_text = cursor.selectedText() # this returns newlines as unicode
            if (u"\u2029" in selected_text): # convert the page break separator (unicode) back to newline character
                selected_text = "\n" # replace with newline character
            temp_run = paragraph.add_run(selected_text)
            apply_formatting(cursor_format, temp_run)

    return doc


# def get_text_formatting(editor_document: QTextDocument):
#     cursor = QTextCursor(editor_document)

#     formatted_document = []
#     current_character_index = 0

#     while not cursor.atEnd():
#         cursor.setPosition(current_character_index)
#         cursor.movePosition(
#             QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor
#         )


#         # if len(cursor.selectedText()) == 1:
#             # print("single character", cursor.selection())
#             # cursor_selection = cursor.charFormat()
#             # if cursor_selection.isCharFormat():
#             #     print(cursor_selection)
#             #     char_format = cursor.charFormat()
#             #     formatted_document.append((
#             #         char_format,
#             #         {
#             #             "bold": (
#             #                 True
#             #                 if char_format.fontWeight() == QFont.Weight.Bold
#             #                 else False
#             #             ),
#             #             "italic": char_format.fontItalic(),
#             #             "underline": char_format.fontUnderline(),
#             #         },
#             #     ))
#             # elif cursor.IsImageFormat():
#             #     print(cursor_selection.toImageFormat())
#             #     print("image format")
#             # else:
#             #     print("unknown format")
#         current_character_index += 1

#     return formatted_document


# def convert_to_docx(editor_document: QTextDocument):
#     text_format = get_text_formatting(editor_document)

#     print(text_format)

#     document = Document()
#     paragraph = document.add_paragraph()
#     for run_text, font_format in text_format:
#         print(run_text, font_format)
#         run = paragraph.add_run(run_text)
#         if text_format["bold"]:
#             run.bold = True
#         if text_format["italic"]:
#             run.italic = True
#         if text_format["underline"]:
#             run.underline = True

#         # if text_format[i]["bold"]:
#         #     document.add_paragraph(editor_document.toPlainText()[i], style="Bold")
#         # elif text_format[i]["italic"]:
#         #     document.add_paragraph(editor_document.toPlainText()[i], style="Italic")
#         # elif text_format[i]["underline"]:
#         #     document.add_paragraph(editor_document.toPlainText()[i], style="Underline")
#         # else:
#         #     document.add_paragraph(editor_document.toPlainText()[i])

#     return document
