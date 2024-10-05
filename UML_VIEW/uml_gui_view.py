import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QLabel, QWidget
from UML_VIEW.uml_observer import UMLObserver as Observer

class MainWindow(QMainWindow, Observer):
    def __init__(self, interface):
        super().__init__()
        QWidget.__init__(self)  # Initialize QWidget
        self.interface = interface  # Interface to communicate with UMLCoreManager
        uic.loadUi('prototype_gui.ui', self)
        
        # Find "Save As" / "Open" actions
        self.save_button = self.findChild(QAction, "SaveAs")
        self.open_button = self.findChild(QAction, "Open")
        self.label = self.findChild(QLabel, "label")
        
        # Connect the "Save As" action to the click_save_as method
        self.save_button.triggered.connect(self.click_save_as)
        # Connect the "Open" action to the click_save_as method
        self.open_button.triggered.connect(self.click_save_as)

    # Move the click_save_as function outside the __init__ to make it a class method
    def click_save_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save As", "", "All Files (*);; Python Files (*.py);; JSON Files (*.json)")
        if not file_path:
            return
        self.label.setText(str(file_path))
        filename_with_extension = os.path.basename(file_path)
        filename_without_extension, _ = os.path.splitext(filename_with_extension)
        self.interface.save_gui(filename_without_extension, file_path)
        
    def click_open(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Open", "", "All Files (*);; Python Files (*.py);; JSON Files (*.json)")
        if file_name:
            self.label.setText(str(file_name))

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
