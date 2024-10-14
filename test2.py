import sys
from PyQt5 import QtWidgets, QtGui, QtCore

# Custom QGraphicsView that handles rubber band selection
class GridGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.rubber_band = None
        self.is_using_rubber_band = False
        self.origin_point = QtCore.QPointF()

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if isinstance(item, UMLClassBox):
            self.is_using_rubber_band = False
        else:
            self.is_using_rubber_band = True

        if event.button() == QtCore.Qt.LeftButton and self.is_using_rubber_band:
            self.origin_point = event.pos()
            self.rubber_band = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self.viewport())
            self.rubber_band.setGeometry(QtCore.QRect(self.origin_point, QtCore.QSize()))
            self.rubber_band.show()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_using_rubber_band and self.rubber_band:
            rect = QtCore.QRect(self.origin_point.toPoint(), event.pos()).normalized()
            self.rubber_band.setGeometry(rect)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.rubber_band:
            self.rubber_band.hide()
            self.rubber_band = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)

# Custom resize handle class that accepts mouse events
class ResizeHandle(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, handle_name, parent=None):
        super().__init__(parent)
        self.handle_name = handle_name
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

    def mousePressEvent(self, event):
        event.accept()

    def mouseMoveEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        event.accept()

# Custom UMLClassBox that can be resized and moved
class UMLClassBox(QtWidgets.QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRect(0, 0, 150, 100)
        self.setBrush(QtGui.QBrush(QtGui.QColor(200, 200, 255)))
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setAcceptHoverEvents(True)

        self.is_resizing = False
        self.current_handle = None
        self.is_box_dragged = False

        self.handle_size = 10
        self.create_resize_handles()
        self.update_handle_positions()

    def create_resize_handles(self):
        self.handles_list = {
            'top_left': ResizeHandle('top_left', self),
            'top_right': ResizeHandle('top_right', self),
            'bottom_left': ResizeHandle('bottom_left', self),
            'bottom_right': ResizeHandle('bottom_right', self),
        }

        for handle_name, handle in self.handles_list.items():
            handle.setRect(-self.handle_size / 2, -self.handle_size / 2, self.handle_size, self.handle_size)
            handle.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
            handle.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            handle.setZValue(1)  # Ensure handles are on top

    def update_handle_positions(self):
        rect = self.rect()
        self.handles_list['top_left'].setPos(rect.topLeft())
        self.handles_list['top_right'].setPos(rect.topRight())
        self.handles_list['bottom_left'].setPos(rect.bottomLeft())
        self.handles_list['bottom_right'].setPos(rect.bottomRight())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if isinstance(event.target(), ResizeHandle):
                handle = event.target()
                self.current_handle = handle.handle_name
                self.is_resizing = True
                event.accept()
            else:
                self.is_box_dragged = True
                super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_resizing and self.current_handle:
            self.resize_box(event)
            event.accept()
        elif self.is_box_dragged:
            super().mouseMoveEvent(event)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.is_resizing:
            self.is_resizing = False
            self.current_handle = None
            event.accept()
        elif self.is_box_dragged:
            self.is_box_dragged = False
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def resize_box(self, event):
        pos = self.mapFromScene(event.scenePos())
        rect = self.rect()

        if self.current_handle == 'top_left':
            new_rect = QtCore.QRectF(pos, rect.bottomRight()).normalized()
        elif self.current_handle == 'top_right':
            new_rect = QtCore.QRectF(QtCore.QPointF(rect.left(), pos.y()), QtCore.QPointF(pos.x(), rect.bottom())).normalized()
        elif self.current_handle == 'bottom_left':
            new_rect = QtCore.QRectF(QtCore.QPointF(pos.x(), rect.top()), QtCore.QPointF(rect.right(), pos.y())).normalized()
        elif self.current_handle == 'bottom_right':
            new_rect = QtCore.QRectF(rect.topLeft(), pos).normalized()
        else:
            return

        min_size = 50  # Minimum size to prevent inversion
        if new_rect.width() < min_size or new_rect.height() < min_size:
            return

        self.prepareGeometryChange()
        self.setRect(new_rect)
        self.update_handle_positions()

# Main application
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        scene = QtWidgets.QGraphicsScene()
        self.view = GridGraphicsView(scene)
        self.setCentralWidget(self.view)

        # Add some UMLClassBoxes to the scene
        box1 = UMLClassBox()
        box1.setPos(50, 50)
        scene.addItem(box1)

        box2 = UMLClassBox()
        box2.setPos(250, 150)
        scene.addItem(box2)

        self.setWindowTitle("UML Class Box with Rubber Band Selection")
        self.resize(600, 400)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
