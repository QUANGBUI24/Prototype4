import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class StylePanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set up the layout for the panel
        layout = QtWidgets.QVBoxLayout(self)
        
        # Font combo box
        self.font_combo = QtWidgets.QFontComboBox(self)
        layout.addWidget(self.font_combo)
        
        # Font size spin box
        self.font_size_spin = QtWidgets.QSpinBox(self)
        self.font_size_spin.setRange(8, 72)  # Font size range
        self.font_size_spin.setValue(12)  # Default font size
        layout.addWidget(self.font_size_spin)
        
        # Bold, Italic, Underline buttons
        self.bold_button = QtWidgets.QPushButton("B", self)
        self.bold_button.setCheckable(True)
        bold_font = QtGui.QFont("Arial", 10)
        bold_font.setBold(True)
        self.bold_button.setFont(bold_font)
        
        self.italic_button = QtWidgets.QPushButton("I", self)
        self.italic_button.setCheckable(True)
        italic_font = QtGui.QFont("Arial", 10)
        italic_font.setItalic(True)
        self.italic_button.setFont(italic_font)
        
        self.underline_button = QtWidgets.QPushButton("U", self)
        self.underline_button.setCheckable(True)
        underline_font = QtGui.QFont("Arial", 10)
        underline_font.setUnderline(True)
        self.underline_button.setFont(underline_font)
        
        # Layout for bold, italic, underline
        format_layout = QtWidgets.QHBoxLayout()
        format_layout.addWidget(self.bold_button)
        format_layout.addWidget(self.italic_button)
        format_layout.addWidget(self.underline_button)
        layout.addLayout(format_layout)
        
        # Alignment buttons (left, center, right)
        self.left_align_button = QtWidgets.QPushButton("Left", self)
        self.left_align_button.setCheckable(True)
        self.center_align_button = QtWidgets.QPushButton("Center", self)
        self.center_align_button.setCheckable(True)
        self.right_align_button = QtWidgets.QPushButton("Right", self)
        self.right_align_button.setCheckable(True)
        
        # Layout for alignment buttons
        align_layout = QtWidgets.QHBoxLayout()
        align_layout.addWidget(self.left_align_button)
        align_layout.addWidget(self.center_align_button)
        align_layout.addWidget(self.right_align_button)
        layout.addLayout(align_layout)
        
        # Font color button
        self.font_color_button = QtWidgets.QPushButton("Font Color", self)
        self.font_color_button.clicked.connect(self.change_font_color)
        layout.addWidget(self.font_color_button)
        
        # Background color button
        self.bg_color_button = QtWidgets.QPushButton("Background Color", self)
        self.bg_color_button.clicked.connect(self.change_background_color)
        layout.addWidget(self.bg_color_button)
        
        # Set the main layout
        self.setLayout(layout)
    
    def change_font_color(self):
        """
        Opens a color dialog to select the font color.
        """
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.font_color_button.setStyleSheet(f"background-color: {color.name()};")

    def change_background_color(self):
        """
        Opens a color dialog to select the background color.
        """
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.bg_color_button.setStyleSheet(f"background-color: {color.name()};")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the central widget and layout
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # Add style panel on the right side
        self.style_panel = StylePanel(self)
        self.central_layout.addWidget(self.style_panel)

        # Placeholder for canvas or other content
        self.canvas = QtWidgets.QLabel("Canvas Area", self)
        self.canvas.setAlignment(QtCore.Qt.AlignCenter)
        self.canvas.setFixedSize(400, 300)
        self.central_layout.addWidget(self.canvas)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
