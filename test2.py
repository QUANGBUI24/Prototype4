import sys
from PyQt5 import QtCore, QtWidgets, QtGui

class UMLHandle(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, box, handle_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = box  # Keep reference to the UMLClassBox
        self.handle_name = handle_name

        # Set handle appearance
        self.setRect(-5, -5, 10, 10)  # Small circle handles
        self.setPen(QtGui.QPen(QtGui.QColor(30, 144, 255)))  # Blue border
        self.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))  # White fill

        # Set handle properties
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        """Change cursor when hovering over the handle."""
        if self.handle_name in ['top_left', 'bottom_right']:
            self.box.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif self.handle_name in ['top_right', 'bottom_left']:
            self.box.setCursor(QtCore.Qt.SizeBDiagCursor)
        event.accept()

    def hoverLeaveEvent(self, event):
        """Reset cursor when leaving the handle."""
        self.box.setCursor(QtCore.Qt.ArrowCursor)
        event.accept()

    def mousePressEvent(self, event):
        """Handle mouse press events for resizing the box."""
        self.box.start_resizing(self.handle_name)
        event.accept()

class UMLClassBox(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set box appearance and default size
        self.setRect(50, 50, 150, 100)
        self.setPen(QtGui.QPen(QtGui.QColor(30, 144, 255)))
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))

        # Enable box selection and movement
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

        # Track resizing state
        self.is_resizing = False
        self.current_handle = None
        self.handle_offset = 20  # Move handles away from corners by 20 pixels

        # Initialize handles_list to store the handles
        self.handles = {}

    def create_handles(self):
        """Create handles for resizing the box."""
        self.handles = {
            'top_left': UMLHandle(self, 'top_left'),
            'top_right': UMLHandle(self, 'top_right'),
            'bottom_left': UMLHandle(self, 'bottom_left'),
            'bottom_right': UMLHandle(self, 'bottom_right'),
        }
        for handle in self.handles.values():
            self.scene().addItem(handle)  # Add handles to the scene

        self.update_handle_positions()

    def update_handle_positions(self):
        """Update the position of the resize handles."""
        rect = self.rect()
        offset = self.handle_offset

        # Move handles outside the box by the offset value
        self.handles['top_left'].setPos(rect.topLeft().x() - offset, rect.topLeft().y() - offset)
        self.handles['top_right'].setPos(rect.topRight().x() + offset, rect.topRight().y() - offset)
        self.handles['bottom_left'].setPos(rect.bottomLeft().x() - offset, rect.bottomLeft().y() + offset)
        self.handles['bottom_right'].setPos(rect.bottomRight().x() + offset, rect.bottomRight().y() + offset)

    def start_resizing(self, handle_name):
        """Start resizing the box based on the handle."""
        self.is_resizing = True
        self.current_handle = handle_name

    def mouseMoveEvent(self, event):
        """Handle resizing based on the handle being dragged."""
        if self.is_resizing and self.current_handle:
            pos = self.mapFromScene(event.scenePos())
            new_rect = self.rect()

            if self.current_handle == 'top_left':
                new_rect.setTopLeft(pos)
            elif self.current_handle == 'top_right':
                new_rect.setTopRight(pos)
            elif self.current_handle == 'bottom_left':
                new_rect.setBottomLeft(pos)
            elif self.current_handle == 'bottom_right':
                new_rect.setBottomRight(pos)

            self.setRect(new_rect)
            self.update_handle_positions()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Stop resizing when the mouse is released."""
        self.is_resizing = False
        self.current_handle = None
        super().mouseReleaseEvent(event)

    def itemChange(self, change, value):
        """Check when the UMLClassBox is added to the scene."""
        if change == QtWidgets.QGraphicsItem.ItemSceneChange:
            if self.scene() is not None:
                self.create_handles()  # Create handles only after the box is added to the scene
        return super().itemChange(change, value)


class UMLScene(QtWidgets.QGraphicsScene):
    """A custom QGraphicsScene that handles multiple UML boxes."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSceneRect(0, 0, 800, 600)

        # Create a UMLClassBox and add it to the scene
        box = UMLClassBox()
        self.addItem(box)


class UMLView(QtWidgets.QGraphicsView):
    """A custom QGraphicsView to visualize the UMLScene."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setScene(UMLScene())

        # Enable antialiasing for smoother visuals
        self.setRenderHint(QtGui.QPainter.Antialiasing)


class UMLApp(QtWidgets.QApplication):
    """The main application."""
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        # Create the main window with a UMLView
        self.main_window = QtWidgets.QMainWindow()
        self.view = UMLView()
        self.main_window.setCentralWidget(self.view)
        self.main_window.resize(800, 600)
        self.main_window.show()


if __name__ == "__main__":
    app = UMLApp(sys.argv)
    sys.exit(app.exec_())
