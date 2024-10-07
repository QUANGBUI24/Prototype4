import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class UMLClassBox(QtWidgets.QGraphicsRectItem):
    def __init__(self, class_name="Class_Name", fields=None, methods=None, parent=None):
        super().__init__(parent)
        self.default_width = 200
        self.default_margin = 10
        self.setRect(0, 0, self.default_width, 300)
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 2, QtCore.Qt.DashLine))
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))

        # Default fields and methods if not provided
        if fields is None:
            fields = ["Field_1", "Field_2"]
        if methods is None:
            methods = ["Method_1\n    param_1\n    param_2", "Method_2"]

        # Editable class name
        self.class_name_text = QtWidgets.QGraphicsTextItem(self)
        self.class_name_text.setPlainText(class_name)
        self.class_name_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.class_name_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.class_name_text.setPos(self.default_margin, self.default_margin)
        self.class_name_text.document().contentsChanged.connect(self.update_positions)

        # Editable fields
        self.fields_label = QtWidgets.QGraphicsTextItem(self)
        self.fields_label.setPlainText("Fields")
        self.fields_label.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.fields_label.setPos(self.default_margin, 40)

        self.fields_text = QtWidgets.QGraphicsTextItem(self)
        self.fields_text.setPlainText("\n".join(fields))
        self.fields_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.fields_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.fields_text.setPos(self.default_margin + 10, 60)
        self.fields_text.document().contentsChanged.connect(self.update_positions)

        # Editable methods
        self.methods_label = QtWidgets.QGraphicsTextItem(self)
        self.methods_label.setPlainText("Methods")
        self.methods_label.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.methods_label.setPos(self.default_margin, 140)

        self.methods_text = QtWidgets.QGraphicsTextItem(self)
        self.methods_text.setPlainText("\n".join(methods))
        self.methods_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.methods_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.methods_text.setPos(self.default_margin + 10, 160)
        self.methods_text.document().contentsChanged.connect(self.update_positions)

        # Separators
        self.separator_lines = []
        self.create_separator_lines()

        # Update initial positions
        self.update_positions()

    def create_separator_lines(self):
        # Create two separators for class sections
        self.separator_lines = [
            QtWidgets.QGraphicsLineItem(self),
            QtWidgets.QGraphicsLineItem(self)
        ]
        for line in self.separator_lines:
            line.setPen(QtGui.QPen(QtCore.Qt.black))

    def update_positions(self):
        # Update the height of each section dynamically
        class_name_height = self.class_name_text.boundingRect().height() + self.default_margin
        fields_label_height = self.fields_label.boundingRect().height() + self.default_margin
        fields_text_height = self.fields_text.boundingRect().height() + self.default_margin
        methods_label_height = self.methods_label.boundingRect().height() + self.default_margin

        # Update position of fields label and text
        self.fields_label.setPos(self.default_margin, class_name_height + 5)
        self.fields_text.setPos(self.default_margin + 10, class_name_height + fields_label_height)

        # Update position of methods label and text
        methods_y = class_name_height + fields_label_height + fields_text_height + 10
        self.methods_label.setPos(self.default_margin, methods_y)
        self.methods_text.setPos(self.default_margin + 10, methods_y + methods_label_height)

        # Update separator lines
        self.separator_lines[0].setLine(0, class_name_height, self.rect().width(), class_name_height)
        self.separator_lines[1].setLine(0, methods_y, self.rect().width(), methods_y)

        # Update the bounding box width to fit the longest content
        max_width = max(
            self.default_width,
            self.class_name_text.boundingRect().width() + 2 * self.default_margin,
            self.fields_text.boundingRect().width() + 2 * self.default_margin + 10,
            self.methods_text.boundingRect().width() + 2 * self.default_margin + 10
        )

        # Update the bounding box height to fit all content
        total_height = methods_y + methods_label_height + self.methods_text.boundingRect().height() + self.default_margin

        # Set new rectangle with updated width and height
        self.setRect(0, 0, max_width, total_height)


class UMLDiagramScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 800, 600)

        # Add UML Class Box
        self.uml_class_box = UMLClassBox()
        self.addItem(self.uml_class_box)


class UMLDiagramView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        scene = UMLDiagramScene(parent)
        super().__init__(scene, parent)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setScene(scene)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UML Diagram Editor")
        self.setGeometry(100, 100, 800, 600)

        # Create UML Diagram View
        self.uml_view = UMLDiagramView(self)
        self.setCentralWidget(self.uml_view)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
