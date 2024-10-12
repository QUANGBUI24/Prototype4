import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class Box(QtWidgets.QGraphicsRectItem):
    def __init__(self):
        super().__init__(QtCore.QRectF(50, 50, 100, 100))  # Box size and position
        self.setBrush(QtGui.QBrush(QtGui.QColor(100, 100, 250)))
    
    def contextMenuEvent(self, event):
        # Create the pop-up menu
        menu = QtWidgets.QMenu()

        # Add options to the menu
        add_field_action = menu.addAction('Add Field')
        add_method_action = menu.addAction('Add Method')
        add_parameter_action = menu.addAction('Add Parameter')

        # Show the menu at the cursor position
        action = menu.exec_(event.screenPos())
        
        # Connect actions to methods
        if action == add_field_action:
            self.add_field()
        elif action == add_method_action:
            self.add_method()
        elif action == add_parameter_action:
            self.add_parameter()

    def add_field(self):
        print("Field added!")

    def add_method(self):
        print("Method added!")

    def add_parameter(self):
        print("Parameter added!")

class Scene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super().__init__()
        # Add a box to the scene
        self.box = Box()
        self.addItem(self.box)
        
class MainWindow(QtWidgets.QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = Scene()
        self.setScene(self.scene)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
