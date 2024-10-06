from PyQt5 import QtWidgets, QtGui, QtCore
import sys


class SimpleGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the scene
        self.scene = QtWidgets.QGraphicsScene(parent)
        self.setScene(self.scene)
        self.setSceneRect(-500, -500, 1000, 1000)

        # Set the initial mode (light mode by default)
        self.is_dark_mode = False
        self.setLightMode()

    def setLightMode(self):
        """
        Sets the view to light mode.
        """
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))  # White background
        self.is_dark_mode = False
        self.viewport().update()
        self.scene.update()

    def setDarkMode(self):
        """
        Sets the view to dark mode.
        """
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))  # Dark background
        self.is_dark_mode = True
        self.viewport().update()
        self.scene.update()

    def toggleMode(self):
        """
        Toggles between dark mode and light mode.
        """
        if self.is_dark_mode:
            self.setLightMode()
        else:
            self.setDarkMode()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create the custom graphics view
        self.graphics_view = SimpleGraphicsView()

        # Create a button to toggle between light and dark modes
        self.toggle_button = QtWidgets.QPushButton("Toggle Dark/Light Mode")
        self.toggle_button.clicked.connect(self.graphics_view.toggleMode)

        # Set up the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.graphics_view)
        layout.addWidget(self.toggle_button)

        self.setLayout(layout)
        self.setWindowTitle("Light/Dark Mode Toggle Example")
        self.resize(800, 600)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
