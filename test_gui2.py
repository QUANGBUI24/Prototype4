# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtGui import QFontDatabase

# # Create an instance of QApplication
# app = QApplication([])

# # Get all the fonts available on the system
# font_database = QFontDatabase()
# fonts = font_database.families()

# # Print the list of fonts
# for font in fonts:
#     print(font)

# # Exit the application
# app.quit()


import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the .ui file
        uic.loadUi('prototype_gui.ui', self)  # Make sure the file is in the same directory or provide the correct path

# Create an instance of QApplication
app = QApplication(sys.argv)

# Create an instance of your main window class
window = MainWindow()

# Show the main window
window.show()

# Execute the application's event loop
sys.exit(app.exec_())

