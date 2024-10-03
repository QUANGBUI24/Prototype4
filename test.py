from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

# Create an instance of QApplication
app = QApplication([])

# Get all the fonts available on the system
font_database = QFontDatabase()
fonts = font_database.families()

# Print the list of fonts
for font in fonts:
    print(font)

# Exit the application
app.quit()
