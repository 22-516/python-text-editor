import os
import random
import base64

from PyQt6.QtCore import *  # temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

IMAGE_EXTENSIONS = [
    str(file_extension, "utf-8")
    for file_extension in QImageReader.supportedImageFormats()
]


class TextEditor(QTextEdit):
    def __init__(self, file_path=""):
        super().__init__()

        self.file_path = file_path
        _1, file_extension = os.path.splitext(file_path)
        self.file_name = os.path.basename(file_path) or "New Document"
        self.file_extension = file_extension or None

        randomTestingPageId = str(random.randint(1, 100))  # testing new tabs
        for _ in range(9):
            self.append("testing " + randomTestingPageId)

        self.document().setModified(
            False
        )  # temporary to allow for placeholder text on launch

    def canInsertFromMimeData(self, source):
        if source.hasImage():
            return True
        else:
            return super().canInsertFromMimeData(source)
            # return super(TextEditor, self).canInsertFromMimeData(source)

    def createMimeDataFromSelection(self):
        cursor = self.textCursor()
        if (
            len(cursor.selectedText()) == 1
        ):  # if only one character is selected, check if it's an image
            cursor.setPosition(cursor.selectionEnd())
            fmt = cursor.charFormat()
            # print(fmt)
            if fmt.isImageFormat():
                fmt = (
                    fmt.toImageFormat()
                )  # if selection is an image, convert to QTextImageFormat
                print(fmt.name())
                url = QUrl(fmt.name())
                image = self.document().resource(
                    QTextDocument.ResourceType.ImageResource, url
                )
                mime = QMimeData()
                mime.setImageData(image)
                return mime
        return super().createMimeDataFromSelection()

    def insertImage(self, image):
        if image.isNull():
            return False
        if isinstance(image, QPixmap):  # if image is a QPixmap, convert to QImage
            image = image.toImage()

        doc = self.document()
        if image.width() > doc.pageSize().width():
            image = image.scaledToWidth(
                int(doc.pageSize().width()), Qt.SmoothTransformation
            )

        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        image.save(buffer, "PNG", quality=95)
        binary = base64.b64encode(byte_array.data())
        html_bin = '<img src= "data:image/*;base64,{}" max-width=100% max-height=100%></img>'.format(
            str(binary, "utf-8")
        )
        self.textCursor().insertHtml(html_bin)

        return True

    def insertFromMimeData(self, source: QMimeData):
        if source.hasImage() and self.insertImage(source.imageData()):
            return
        elif source.hasUrls():
            for url in source.urls():
                if not url.isLocalFile():
                    continue
                path = url.toLocalFile()
                info = QFileInfo(path)
                if not info.suffix().lower() in IMAGE_EXTENSIONS:
                    continue
                elif self.insertImage(QImage(path)):
                    return
        super().insertFromMimeData(source)

    def user_insert_image(self, image_path):  # testing
        cursor = QTextCursor(self.textCursor())
        image_format = QTextImageFormat()
        image_format.setName(image_path)
        cursor.insertImage(image_format)

    def set_file_path(self, file_path=""):
        self.file_path = file_path
        _1, file_extension = os.path.splitext(file_path)
        self.file_name = os.path.basename(file_path) or "New Document"
        self.file_extension = file_extension or None

    # text formatting

    def font_bold(self):
        font_weight = self.fontWeight()
        return font_weight == QFont.Weight.Bold

    def font_size(self):
        # font_size = str(self.fontPointSize()).split('.', maxsplit=1)[0]
        # print(font_size)
        font_size = f"{self.currentFont().pointSizeF():g}"
        # print(font_size)
        return font_size

    def toggle_selected_bold(self):
        # self.setFontWeight(new_font_weight := QFont.Weight.Bold if self.fontWeight() == QFont.Weight.Normal else QFont.Weight.Normal)
        self.setFontWeight(
            new_font_weight := (
                QFont.Weight.Bold if not self.font_bold() else QFont.Weight.Normal
            )
        )
        return new_font_weight

    def toggle_selected_underline(self):
        self.setFontUnderline(new_font_underline := not self.fontUnderline())
        return new_font_underline

    def toggle_selected_italics(self):
        self.setFontItalic(new_font_italics := not self.fontItalic())
        return new_font_italics

    def change_font(self, new_font: QFont):
        # we do this convoluted method rather than just calling setFont() because we want to preserve the other formatting
        # (e.g. bold, underline, italics, colour, highlight)
        cursor = self.textCursor()

        selection_end = cursor.selectionEnd()
        selection_start = cursor.selectionStart()

        cursor.setPosition(selection_start)

        while (
            cursor.position() < selection_end and cursor.position() >= selection_start
        ):
            new_format = QTextCharFormat()
            new_format.setFont(new_font)
            new_format.setFontPointSize(cursor.charFormat().font().pointSizeF())
            new_format.setFontWeight(cursor.charFormat().font().weight())
            new_format.setFontItalic(cursor.charFormat().font().italic())
            new_format.setFontUnderline(cursor.charFormat().font().underline())
            new_format.setBackground(cursor.charFormat().background())
            new_format.setForeground(cursor.charFormat().foreground())
            cursor.mergeCharFormat(new_format)
            cursor.movePosition(
                QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.MoveAnchor
            )
            cursor.movePosition(
                QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor
            )

    def change_highlight(self, new_highlight):
        if self.textBackgroundColor() == new_highlight:
            # self.setTextBackgroundColor(QColor())
            self.setTextBackgroundColor(QColor().fromRgb(255, 255, 255, 1))
        else:
            self.setTextBackgroundColor(new_highlight)

    def change_color(self, new_colour):
        self.setTextColor(new_colour)

    def change_font_size(self, new_font_size):
        try:
            font_size = float(new_font_size)
        except ValueError:  # if cant be converted to float (empty string)
            return
        self.setFontPointSize(font_size)
