import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QToolBar, QColorDialog, QFontComboBox, QComboBox, QLabel
)
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtCore import Qt


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up main window properties
        self.setWindowTitle("Simple Text Editor")
        self.setGeometry(100, 100, 800, 600)

        # Set up the text edit widget
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Create the toolbar for editing options
        self.create_toolbar()

    def create_toolbar(self):
        # Create a toolbar
        toolbar = QToolBar("Text Editing Toolbar", self)
        self.addToolBar(toolbar)

        # Font selection combo box
        font_combobox = QFontComboBox(self)
        font_combobox.currentFontChanged.connect(self.change_font)
        toolbar.addWidget(QLabel("Font: "))
        toolbar.addWidget(font_combobox)

        # Font size combo box
        font_size_combobox = QComboBox(self)
        font_size_combobox.setEditable(True)
        font_size_combobox.addItems([str(size) for size in range(8, 30, 2)])
        font_size_combobox.setCurrentText("12")
        font_size_combobox.currentTextChanged.connect(self.change_font_size)
        toolbar.addWidget(QLabel("Size: "))
        toolbar.addWidget(font_size_combobox)

        # Bold action
        bold_action = QAction(QIcon(), "Bold", self)
        bold_action.setCheckable(True)
        bold_action.triggered.connect(self.toggle_bold)
        toolbar.addAction(bold_action)

        # Italic action
        italic_action = QAction(QIcon(), "Italic", self)
        italic_action.setCheckable(True)
        italic_action.triggered.connect(self.toggle_italic)
        toolbar.addAction(italic_action)

        # Underline action
        underline_action = QAction(QIcon(), "Underline", self)
        underline_action.setCheckable(True)
        underline_action.triggered.connect(self.toggle_underline)
        toolbar.addAction(underline_action)

        # Text color action
        color_action = QAction(QIcon(), "Text Color", self)
        color_action.triggered.connect(self.change_text_color)
        toolbar.addAction(color_action)

    def change_font(self, font):
        """Change the font of the selected text."""
        self.text_edit.setCurrentFont(font)

    def change_font_size(self, size):
        """Change the font size of the selected text."""
        try:
            size = int(size)
            self.text_edit.setFontPointSize(size)
        except ValueError:
            pass  # Ignore invalid size entries

    def toggle_bold(self, checked):
        """Toggle bold formatting on selected text."""
        if checked:
            self.text_edit.setFontWeight(QFont.Bold)
        else:
            self.text_edit.setFontWeight(QFont.Normal)

    def toggle_italic(self, checked):
        """Toggle italic formatting on selected text."""
        self.text_edit.setFontItalic(checked)

    def toggle_underline(self, checked):
        """Toggle underline formatting on selected text."""
        self.text_edit.setFontUnderline(checked)

    def change_text_color(self):
        """Open a color dialog to change the text color."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextColor(color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
