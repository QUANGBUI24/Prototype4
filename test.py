from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem
from PyQt5.QtGui import QBrush, QPen, QPainter
from PyQt5.QtCore import Qt, QRectF, QPointF

class ResizableUMLClass(QGraphicsRectItem):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        
        self.handle_size = 10.0
        self.handles = {
            'top_left': QRectF(0, 0, self.handle_size, self.handle_size),
            'top_right': QRectF(0, 0, self.handle_size, self.handle_size),
            'bottom_left': QRectF(0, 0, self.handle_size, self.handle_size),
            'bottom_right': QRectF(0, 0, self.handle_size, self.handle_size)
        }
        self.current_handle = None
        self.is_resizing = False
        self.updateHandlesPosition()

    def updateHandlesPosition(self):
        rect = self.rect()
        self.handles['top_left'].moveTo(rect.topLeft())
        self.handles['top_right'].moveTo(rect.topRight() - QPointF(self.handle_size, 0))
        self.handles['bottom_left'].moveTo(rect.bottomLeft() - QPointF(0, self.handle_size))
        self.handles['bottom_right'].moveTo(rect.bottomRight() - QPointF(self.handle_size, self.handle_size))

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        # Draw the resize handles
        if self.isSelected():
            painter.setBrush(Qt.black)
            for handle_rect in self.handles.values():
                painter.drawRect(handle_rect)

    def hoverMoveEvent(self, event):
        cursor = Qt.ArrowCursor
        for handle_name, handle_rect in self.handles.items():
            if handle_rect.contains(event.pos()):
                cursor = Qt.SizeFDiagCursor
                break
        self.setCursor(cursor)
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        self.is_resizing = False
        for handle_name, handle_rect in self.handles.items():
            if handle_rect.contains(event.pos()):
                self.current_handle = handle_name
                self.is_resizing = True
                break
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_resizing and self.current_handle:
            new_rect = QRectF(self.rect())
            if self.current_handle == 'top_left':
                new_rect.setTopLeft(event.pos())
            elif self.current_handle == 'top_right':
                new_rect.setTopRight(event.pos())
            elif self.current_handle == 'bottom_left':
                new_rect.setBottomLeft(event.pos())
            elif self.current_handle == 'bottom_right':
                new_rect.setBottomRight(event.pos())

            # Ensure a minimum size
            if new_rect.width() > 20 and new_rect.height() > 20:
                self.setRect(new_rect)
                self.updateHandlesPosition()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.is_resizing = False
        self.current_handle = None
        super().mouseReleaseEvent(event)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    uml_class = ResizableUMLClass(50, 50, 200, 100)
    uml_class.setPen(QPen(Qt.black))
    uml_class.setBrush(QBrush(Qt.lightGray))
    scene.addItem(uml_class)

    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.setScene(scene)
    view.setFixedSize(600, 400)
    view.show()

    sys.exit(app.exec_())
