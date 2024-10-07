from PyQt5.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem,
    QGraphicsTextItem, QGraphicsProxyWidget, QPushButton,
    QVBoxLayout, QWidget, QInputDialog, QGraphicsItem, QMessageBox
)
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import Qt, QRectF


class UMLDiagram(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the graphics scene and view
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.view)
        self.setLayout(main_layout)

        self.setWindowTitle("Simple UML Diagram with Buttons")
        self.setGeometry(100, 100, 800, 600)

        # Adding the first UML class item to demonstrate functionality
        self.add_uml_class()

    def add_uml_class(self):
        # Create a new UML class box
        class_name, ok = QInputDialog.getText(self, "Add Class", "Enter class name:")
        if ok and class_name:
            uml_class_item = UMLClassItem(class_name)
            self.scene.addItem(uml_class_item)


class UMLClassItem(QGraphicsRectItem):
    def __init__(self, class_name):
        super().__init__(QRectF(0, 0, 250, 400))
        self.setBrush(QColor(173, 216, 230))  # Light blue color
        self.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        # Class Name
        self.class_name_text = QGraphicsTextItem(class_name, self)
        self.class_name_text.setPos(10, 10)

        # Fields Section
        self.fields_label = QGraphicsTextItem("Fields:", self)
        self.fields_label.setPos(10, 50)

        # Fields Buttons (+ and -)
        self.add_field_button = QPushButton("+ Field")
        self.remove_field_button = QPushButton("- Field")
        self.add_field_button_proxy = QGraphicsProxyWidget(self)
        self.remove_field_button_proxy = QGraphicsProxyWidget(self)
        self.add_field_button_proxy.setWidget(self.add_field_button)
        self.remove_field_button_proxy.setWidget(self.remove_field_button)
        self.add_field_button_proxy.setPos(10, 70)
        self.remove_field_button_proxy.setPos(100, 70)

        # Connect Field Buttons
        self.add_field_button.clicked.connect(self.add_field)
        self.remove_field_button.clicked.connect(self.remove_field)

        # Methods Section
        self.methods_label = QGraphicsTextItem("Methods:", self)
        self.methods_label.setPos(10, 120)

        # Methods Buttons (+ and -)
        self.add_method_button = QPushButton("+ Method")
        self.remove_method_button = QPushButton("- Method")
        self.add_method_button_proxy = QGraphicsProxyWidget(self)
        self.remove_method_button_proxy = QGraphicsProxyWidget(self)
        self.add_method_button_proxy.setWidget(self.add_method_button)
        self.remove_method_button_proxy.setWidget(self.remove_method_button)
        self.add_method_button_proxy.setPos(10, 140)
        self.remove_method_button_proxy.setPos(100, 140)

        # Connect Method Buttons
        self.add_method_button.clicked.connect(self.add_method)
        self.remove_method_button.clicked.connect(self.remove_method)

        # Lists to keep track of fields and methods
        self.fields = []
        self.methods = []

    def add_field(self):
        field_name, ok = QInputDialog.getText(None, "Add Field", "Enter field name:")
        if ok and field_name:
            new_field = QGraphicsTextItem(field_name, self)
            new_field.setPos(20, 90 + len(self.fields) * 20)
            self.fields.append(new_field)

    def remove_field(self):
        if self.fields:
            # Show list of current fields for the user to choose which one to delete
            field_names = [field.toPlainText() for field in self.fields]
            field_name, ok = QInputDialog.getItem(None, "Remove Field", "Select field to remove:", field_names, 0, False)
            if ok and field_name:
                # Find the field to remove
                for field in self.fields:
                    if field.toPlainText() == field_name:
                        self.scene().removeItem(field)
                        self.fields.remove(field)
                        break
        else:
            QMessageBox.warning(None, "Warning", "No fields to remove.")

    def add_method(self):
        method_name, ok = QInputDialog.getText(None, "Add Method", "Enter method name:")
        if ok and method_name:
            # Create a MethodItem for adding parameters
            method_item = MethodItem(method_name, self)
            method_item.setPos(20, 170 + len(self.methods) * 60)
            self.methods.append(method_item)

    def remove_method(self):
        if self.methods:
            # Show list of current methods for the user to choose which one to delete
            method_names = [method.method_name_text.toPlainText() for method in self.methods]
            method_name, ok = QInputDialog.getItem(None, "Remove Method", "Select method to remove:", method_names, 0, False)
            if ok and method_name:
                # Find the method to remove
                for method in self.methods:
                    if method.method_name_text.toPlainText() == method_name:
                        self.scene().removeItem(method)
                        self.methods.remove(method)
                        break
        else:
            QMessageBox.warning(None, "Warning", "No methods to remove.")


class MethodItem(QGraphicsRectItem):
    def __init__(self, method_name, parent=None):
        super().__init__(QRectF(0, 0, 200, 60), parent)
        self.setBrush(QColor(255, 255, 200))  # Light yellow color for methods

        # Method Name
        self.method_name_text = QGraphicsTextItem(method_name, self)
        self.method_name_text.setPos(10, 5)

        # Parameters List
        self.parameters = []

        # Parameters Buttons (+ and -)
        self.add_param_button = QPushButton("+ Parameter")
        self.remove_param_button = QPushButton("- Parameter")
        self.add_param_button_proxy = QGraphicsProxyWidget(self)
        self.remove_param_button_proxy = QGraphicsProxyWidget(self)
        self.add_param_button_proxy.setWidget(self.add_param_button)
        self.remove_param_button_proxy.setWidget(self.remove_param_button)
        self.add_param_button_proxy.setPos(10, 30)
        self.remove_param_button_proxy.setPos(110, 30)

        # Connect Parameter Buttons
        self.add_param_button.clicked.connect(self.add_parameter)
        self.remove_param_button.clicked.connect(self.remove_parameter)

    def add_parameter(self):
        param_name, ok = QInputDialog.getText(None, "Add Parameter", "Enter parameter name:")
        if ok and param_name:
            new_param = QGraphicsTextItem(param_name, self)
            new_param.setPos(20, 50 + len(self.parameters) * 20)
            self.parameters.append(new_param)

    def remove_parameter(self):
        if self.parameters:
            # Show list of current parameters for the user to choose which one to delete
            param_names = [param.toPlainText() for param in self.parameters]
            param_name, ok = QInputDialog.getItem(None, "Remove Parameter", "Select parameter to remove:", param_names, 0, False)
            if ok and param_name:
                # Find the parameter to remove
                for param in self.parameters:
                    if param.toPlainText() == param_name:
                        self.scene().removeItem(param)
                        self.parameters.remove(param)
                        break
        else:
            QMessageBox.warning(None, "Warning", "No parameters to remove.")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = UMLDiagram()
    window.show()
    sys.exit(app.exec_())
