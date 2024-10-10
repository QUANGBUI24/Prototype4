import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class UMLTestBox(QtWidgets.QGraphicsRectItem):
    def __init__(self, interface=None, parent=None):
        super().__init__(parent)

        # Initial default size for the box
        self.setRect(100, 100, 200, 100)
        self.handle_size = 10
        self.is_resizing = False
        self.current_handle = None

        # Create the 4 corner handles
        self.create_resize_handles()

        # Set pen and brush
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setAcceptHoverEvents(True)

    def create_resize_handles(self):
        """Create 4 resize handles at the corners."""
        self.handles_list = {
            'top_left': QtWidgets.QGraphicsEllipseItem(self),
            'top_right': QtWidgets.QGraphicsEllipseItem(self),
            'bottom_left': QtWidgets.QGraphicsEllipseItem(self),
            'bottom_right': QtWidgets.QGraphicsEllipseItem(self),
        }

        for handle in self.handles_list.values():
            handle.setRect(-self.handle_size / 2, -self.handle_size / 2, self.handle_size, self.handle_size)
            handle.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
            handle.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            handle.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)

        # Initial handle positions
        self.update_handle_positions()

    def update_handle_positions(self):
        """Update the handle positions based on the new rectangle size."""
        rect = self.rect()
        self.handles_list['top_left'].setPos(rect.topLeft())
        self.handles_list['top_right'].setPos(rect.topRight())
        self.handles_list['bottom_left'].setPos(rect.bottomLeft())
        self.handles_list['bottom_right'].setPos(rect.bottomRight())

    def mousePressEvent(self, event):
        """Detect which handle is pressed."""
        for handle_name, handle in self.handles_list.items():
            if handle.isUnderMouse():
                self.current_handle = handle_name
                self.is_resizing = True
                break
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Resize the box based on the handle being dragged."""
        if self.is_resizing and self.current_handle:
            rect = self.rect()
            pos = self.mapFromScene(event.scenePos())

            if self.current_handle == 'top_left':
                rect.setTopLeft(pos)
            elif self.current_handle == 'top_right':
                rect.setTopRight(pos)
            elif self.current_handle == 'bottom_left':
                rect.setBottomLeft(pos)
            elif self.current_handle == 'bottom_right':
                rect.setBottomRight(pos)

            # Set the new rectangle size
            self.setRect(rect)
            self.update_handle_positions()  # Update handle positions after resizing

        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Reset the resizing state when the mouse is released."""
        if self.is_resizing:
            self.is_resizing = False
            self.current_handle = None
        super().mouseReleaseEvent(event)


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Create a scene and a view
    scene = QtWidgets.QGraphicsScene()
    view = QtWidgets.QGraphicsView(scene)

    # Create an instance of UMLTestBox
    uml_box = UMLTestBox()
    scene.addItem(uml_box)

    # Show the view
    view.setGeometry(100, 100, 800, 600)
    view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
