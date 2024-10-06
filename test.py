import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class UMLClassBox(QtWidgets.QGraphicsRectItem):
    def __init__(self, class_name="ClassName", attributes=None, methods=None, parent=None):
        super().__init__(parent)

        # Default properties for attributes and methods if not provided
        self.attributes = attributes if attributes is not None else []
        self.methods = methods if methods is not None else []

        # Define the bounding rectangle size
        self.setRect(0, 0, 150, 200)
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))  # Black border
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))  # Cyan background

        # Create editable text items for the class name, attributes, and methods
        self.class_name_text = QtWidgets.QGraphicsTextItem(self)
        self.class_name_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.class_name_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.class_name_text.setPlainText(class_name)  # Set class name text

        self.fields_label = QtWidgets.QGraphicsTextItem(self)
        self.fields_label.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.fields_label.setPlainText("Fields")  # Set fields label text

        self.methods_label = QtWidgets.QGraphicsTextItem(self)
        self.methods_label.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.methods_label.setPlainText("Methods")  # Set methods label text

        self.attributes_text = QtWidgets.QGraphicsTextItem(self)
        self.attributes_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.attributes_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.attributes_text.setPlainText("\n".join(self.attributes))  # Set attributes text

        self.methods_text = QtWidgets.QGraphicsTextItem(self)
        self.methods_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.methods_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.methods_text.setPlainText("\n".join(self.methods))  # Set methods text

        # Update positions based on the current box size
        self.update_positions()

    def update_positions(self):
        """Update the positions of text items based on the current box size."""
        rect = self.rect()
        self.class_name_text.setPos(rect.x() + 5, rect.y() + 5)
        self.fields_label.setPos(rect.x() + 5, rect.y() + 35)
        self.attributes_text.setPos(rect.x() + 15, rect.y() + 55)
        self.methods_label.setPos(rect.x() + 5, rect.y() + 120)
        self.methods_text.setPos(rect.x() + 15, rect.y() + 140)

    def get_class_name(self):
        """Return the class name."""
        return self.class_name_text.toPlainText()

    def get_field_names(self):
        """Return a list of field names."""
        return [line.strip() for line in self.attributes_text.toPlainText().split('\n') if line.strip()]

    def get_method_names(self):
        """Return a list of method names."""
        return [line.strip() for line in self.methods_text.toPlainText().split('\n') if line.strip()]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the scene and view
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Create a UMLClassBox instance
        self.uml_class_box = UMLClassBox("MyClass", ["field1", "field2"], ["method1()", "method2()"])
        self.uml_class_box.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)  # Make the box movable
        self.scene.addItem(self.uml_class_box)

        # Create a button to extract information
        self.extract_button = QtWidgets.QPushButton("Extract UML Information")
        self.extract_button.clicked.connect(self.extract_information)
        self.scene.addWidget(self.extract_button)
        self.extract_button.setGeometry(10, 250, 200, 30)

    def extract_information(self):
        """Extract and print UML information."""
        class_name = self.uml_class_box.get_class_name()
        field_names = self.uml_class_box.get_field_names()
        method_names = self.uml_class_box.get_method_names()

        print(f"Class Name: {class_name}")
        print(f"Field Names: {field_names}")
        print(f"Method Names: {method_names}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("UML Class Box Example")
    window.setGeometry(100, 100, 300, 300)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
