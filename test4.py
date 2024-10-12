import sys
import os
from PyQt5 import QtWidgets


class FileDialogApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        # Create a vertical layout
        layout = QtWidgets.QVBoxLayout()

        # Create buttons for loading and saving files
        self.open_button = QtWidgets.QPushButton("Open File")
        self.save_button = QtWidgets.QPushButton("Save File")

        # Connect button signals to their respective functions
        self.open_button.clicked.connect(self.open_file_dialog)
        self.save_button.clicked.connect(self.save_file_dialog)

        # Add buttons to the layout
        layout.addWidget(self.open_button)
        layout.addWidget(self.save_button)

        # Set the layout on the main widget
        self.setLayout(layout)
        self.setWindowTitle("Open and Save File Example")

    def open_file_dialog(self):
        """
        Open a file dialog to select a file.
        """
        # Show an open file dialog and store the selected file path
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd(),
                                                             "All Files (*);;Text Files (*.txt)")
        if file_name:
            QtWidgets.QMessageBox.information(self, "File Selected", f"File: {file_name}")
            print(f"File selected: {file_name}")

    def save_file_dialog(self):
        """
        Open a save file dialog to select a file location for saving.
        """
        # Show a save file dialog and store the selected file path
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", os.getcwd(),
                                                             "All Files (*);;Text Files (*.txt)")
        if file_name:
            # Save logic here (just printing for now)
            with open(file_name, 'w') as f:
                f.write("Sample data to save")
            QtWidgets.QMessageBox.information(self, "File Saved", f"File saved to: {file_name}")
            print(f"File saved to: {file_name}")


def main():
    # Create application
    app = QtWidgets.QApplication(sys.argv)

    # Create main window
    window = FileDialogApp()
    window.show()

    # Start the event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
