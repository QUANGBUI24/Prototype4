import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPen, QBrush, QCursor, QPainter
from PyQt5.QtCore import Qt, QRectF

class UMLClassItem(QGraphicsRectItem):
    def __init__(self, x, y, width, height, class_name="ClassName", grid_size=20):
        super().__init__(x, y, width, height)
        self.grid_size = grid_size
        self.setFlags(QGraphicsRectItem.ItemIsMovable | QGraphicsRectItem.ItemIsSelectable | QGraphicsRectItem.ItemIsFocusable)
        self.setBrush(QBrush(Qt.white))
        self.setPen(QPen(Qt.black))

        # Add class name as text inside the rectangle
        self.class_name_text = QGraphicsTextItem(class_name, self)
        self.class_name_text.setPos(x + 10, y + 10)

    def mouseReleaseEvent(self, event):
        # On release, snap to grid
        self.snap_to_grid()
        super().mouseReleaseEvent(event)

    def snap_to_grid(self):
        """Snaps the UML class to the nearest grid point."""
        current_pos = self.pos()
        new_x = round(current_pos.x() / self.grid_size) * self.grid_size
        new_y = round(current_pos.y() / self.grid_size) * self.grid_size
        self.setPos(new_x, new_y)

class UMLClassDiagram(QGraphicsView):
    def __init__(self):
        super().__init__()

        # Set up the scene with a large initial size
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

        # Enable scrollbars to appear when needed
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        # Start with a default zoom level
        self.zoom_factor = 1.0
        self.grid_size = 20  # Define the grid size (spacing between lines)
        self.selected_class = None  # Track the selected UML class item

        # Set the scene to a larger size initially
        self.scene.setSceneRect(-5000, -5000, 10000, 10000)

    def add_class(self):
        # Create a new UML class box and add it to the scene
        uml_class = UMLClassItem(100, 100, 150, 100, grid_size=self.grid_size)
        self.scene.addItem(uml_class)

    def reset_view(self):
        """Resets the zoom and position to the initial state."""
        self.resetTransform()  # Reset the zoom to its original state
        self.zoom_factor = 1.0  # Reset the zoom factor
        self.centerOn(0, 0)  # Center the view on the origin (initial position)

    def wheelEvent(self, event):
        """Handles the zoom functionality when the mouse wheel is used."""
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        # Check the direction of the wheel event
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        # Apply the zoom
        self.scale(zoom_factor, zoom_factor)

        # Keep track of the zoom factor to prevent over-zooming
        self.zoom_factor *= zoom_factor

        # Optional: Limit zoom levels
        if self.zoom_factor < 0.2:  # Minimum zoom level
            self.zoom_factor = 0.2
            self.resetTransform()
            self.scale(0.2, 0.2)
        elif self.zoom_factor > 5:  # Maximum zoom level
            self.zoom_factor = 5
            self.resetTransform()
            self.scale(5, 5)

    def drawBackground(self, painter, rect):
        """Draw the grid in the background."""
        super().drawBackground(painter, rect)
        # Set up the pen for drawing the grid
        pen = QPen(Qt.lightGray)
        pen.setWidth(1)
        painter.setPen(pen)

        # Get the current scene rectangle
        left = int(rect.left())
        right = int(rect.right())
        top = int(rect.top())
        bottom = int(rect.bottom())

        # Draw vertical grid lines
        for x in range(left - (left % self.grid_size), right, self.grid_size):
            painter.drawLine(x, top, x, bottom)

        # Draw horizontal grid lines
        for y in range(top - (top % self.grid_size), bottom, self.grid_size):
            painter.drawLine(left, y, right, y)

    def mouseMoveEvent(self, event):
        """Forces the view to update while dragging to avoid grid disappearing."""
        super().mouseMoveEvent(event)
        self.viewport().update()

    def resizeEvent(self, event):
        """Resize event to handle expanding the scene."""
        rect = self.mapToScene(self.rect()).boundingRect()

        # If the view reaches the edge of the scene, expand the scene dynamically
        if rect.right() > self.scene.sceneRect().right() or rect.bottom() > self.scene.sceneRect().bottom():
            self.expand_scene()
        super().resizeEvent(event)

    def expand_scene(self):
        """Expand the scene size dynamically when the user scrolls to the edges."""
        current_rect = self.scene.sceneRect()
        new_width = current_rect.width() * 1.5
        new_height = current_rect.height() * 1.5
        self.scene.setSceneRect(current_rect.left(), current_rect.top(), new_width, new_height)

    def mousePressEvent(self, event):
        """Detects which class is clicked and sets it as the selected class."""
        super().mousePressEvent(event)
        item = self.itemAt(event.pos())
        if isinstance(item, UMLClassItem):
            self.selected_class = item
        else:
            self.selected_class = None

    def delete_selected_class(self):
        """Deletes the selected class from the scene."""
        if self.selected_class:
            self.scene.removeItem(self.selected_class)
            self.selected_class = None

class UMLWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UML Diagram with Grid, Snap-to-Grid, and Dynamic Scene Expansion")
        self.setGeometry(100, 100, 900, 700)

        # Create layout and add button
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Add button to create a class
        self.add_class_button = QPushButton("Add UML Class")
        self.add_class_button.clicked.connect(self.add_class_to_diagram)
        layout.addWidget(self.add_class_button)

        # Add button to delete the selected class
        self.delete_class_button = QPushButton("Delete Selected Class")
        self.delete_class_button.clicked.connect(self.delete_selected_class_from_diagram)
        layout.addWidget(self.delete_class_button)

        # Add reset button to reset view
        self.reset_button = QPushButton("Reset View")
        self.reset_button.clicked.connect(self.reset_diagram_view)
        layout.addWidget(self.reset_button)

        # Create the UML diagram view
        self.uml_view = UMLClassDiagram()
        layout.addWidget(self.uml_view)

    def add_class_to_diagram(self):
        # Call the method to add a UML class to the diagram
        self.uml_view.add_class()

    def delete_selected_class_from_diagram(self):
        # Call the method to delete the selected UML class
        self.uml_view.delete_selected_class()

    def reset_diagram_view(self):
        # Call the method to reset the view
        self.uml_view.reset_view()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UMLWindow()
    window.show()
    sys.exit(app.exec_())