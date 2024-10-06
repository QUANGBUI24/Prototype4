###################################################################################################

import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QInputDialog,
                             QGraphicsTextItem, QMainWindow, QVBoxLayout, QPushButton, QGraphicsLineItem,
                             QWidget, QAction, QLabel, QFileDialog, QGraphicsTextItem, QGraphicsSimpleTextItem,
                             QGraphicsRectItem, QGraphicsTextItem, QStyleOptionGraphicsItem, QGraphicsItem, QGraphicsSceneMouseEvent)
from PyQt5.QtGui import QBrush, QPen, QPainter, QCursor
from PyQt5.QtCore import Qt, QRectF, QPointF
from UML_VIEW.uml_observer import UMLObserver as Observer

###################################################################################################

class UMLClassItem(QGraphicsRectItem):
    def __init__(self, x, y, width, height, class_name="ClassName", grid_size=20):
        super().__init__(x, y, width, height)
        self.grid_size = grid_size
        self.setFlags(
            QGraphicsRectItem.ItemIsMovable |
            QGraphicsRectItem.ItemIsSelectable |
            QGraphicsRectItem.ItemIsFocusable |
            QGraphicsRectItem.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        self.setBrush(QBrush(Qt.white))
        self.setPen(QPen(Qt.black))

        # Resizing variables
        self.resizing = False
        self.resize_handle_size = 10
        self.update_resize_handle()  # Update the resize handle's position initially
        self.setCursor(Qt.ArrowCursor)

        # Section heights
        self.section_height = height // 4

        # Create and update text labels for class name, fields, and methods
        self.class_name_text = QGraphicsTextItem(class_name, self)
        self.class_name_text.setTextInteractionFlags(Qt.TextEditorInteraction)  # Editable
        self.update_class_name_position()

        # Create Fields and Methods headers
        self.fields_header = QGraphicsTextItem("+Fields:", self)
        self.update_fields_header_position()

        self.methods_header = QGraphicsTextItem("+Methods:", self)
        self.update_methods_header_position()

        # Divider lines between sections
        self.divider_lines = []
        self.add_divider_lines()

        # Lists to store fields and methods
        self.fields = []
        self.methods = []

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        """Detects double-click events to add a field or method."""
        # Check where the double-click happened relative to the bounding rect
        pos = event.pos()
        rect = self.rect()

        # Determine if the click was in the fields section
        if rect.y() + self.section_height < pos.y() < rect.y() + 2 * self.section_height:
            # Double-click in Fields section
            text, ok = QInputDialog.getText(None, "Add Field", "Enter field name:")
            if ok and text:
                self.add_field(text)

        # Determine if the click was in the methods section
        elif rect.y() + 2 * self.section_height < pos.y() < rect.y() + 3 * self.section_height:
            # Double-click in Methods section
            text, ok = QInputDialog.getText(None, "Add Method", "Enter method name:")
            if ok and text:
                self.add_method(text)

        super().mouseDoubleClickEvent(event)

    def add_field(self, field_name="Field1"):
        """Adds a new field to the fields section and resizes the class box."""
        new_field = QGraphicsTextItem(f"  - {field_name}", self)
        new_field.setTextInteractionFlags(Qt.TextEditorInteraction)  # Make text editable
        self.fields.append(new_field)
        self.update_fields_position()
        self.adjust_height()

    def add_method(self, method_name="Method1"):
        """Adds a new method to the methods section and resizes the class box."""
        new_method = QGraphicsTextItem(f"  - {method_name}:", self)
        new_method.setTextInteractionFlags(Qt.TextEditorInteraction)  # Make text editable
        self.methods.append(new_method)
        self.update_methods_position()
        self.adjust_height()

    def adjust_height(self):
        """Adjust the height of the UML class box to fit the added fields and methods."""
        # Base height is the sum of the sections' heights
        base_height = 3 * self.section_height

        # Add additional height for fields and methods
        field_height = len(self.fields) * 20  # Assuming each field needs 20px height
        method_height = len(self.methods) * 20  # Assuming each method needs 20px height

        # Set the new height
        new_height = base_height + field_height + method_height
        rect = self.rect()
        self.setRect(rect.x(), rect.y(), rect.width(), new_height)

        # Update section heights to redistribute space appropriately
        self.section_height = new_height // 4

        # Update positions and dividers after resizing
        self.update_class_name_position()
        self.update_fields_header_position()
        self.update_methods_header_position()
        self.update_fields_position()
        self.update_methods_position()
        self.update_divider_lines()

    def update_class_name_position(self):
        """Keeps the class name text centered within the top section."""
        rect = self.rect()
        text_width = self.class_name_text.boundingRect().width()
        x_pos = rect.x() + (rect.width() - text_width) / 2
        y_pos = rect.y() + 5
        self.class_name_text.setPos(x_pos, y_pos)

    def update_fields_header_position(self):
        """Position the Fields header."""
        rect = self.rect()
        x_pos = rect.x() + 10
        y_pos = rect.y() + self.section_height + 5
        self.fields_header.setPos(x_pos, y_pos)

    def update_methods_header_position(self):
        """Position the Methods header."""
        rect = self.rect()
        x_pos = rect.x() + 10
        y_pos = rect.y() + 2 * self.section_height + 5
        self.methods_header.setPos(x_pos, y_pos)

    def update_fields_position(self):
        """Update the position of each field below the Fields header."""
        y_offset = self.section_height + 25  # Start below the header
        for index, field in enumerate(self.fields):
            field.setPos(self.rect().x() + 20, self.rect().y() + y_offset + index * 20)

    def update_methods_position(self):
        """Update the position of each method below the Methods header."""
        y_offset = 2 * self.section_height + 25  # Start below the header
        for index, method in enumerate(self.methods):
            method.setPos(self.rect().x() + 20, self.rect().y() + y_offset + index * 20)

    def update_resize_handle(self):
        """Updates the resize handle's position based on the current size of the rectangle."""
        rect = self.rect()
        self.resize_handle_rect = QRectF(
            rect.right() - self.resize_handle_size,
            rect.bottom() - self.resize_handle_size,
            self.resize_handle_size,
            self.resize_handle_size
        )

    def add_divider_lines(self):
        """Add horizontal divider lines to separate sections."""
        rect = self.rect()
        for i in range(1, 4):
            line = QGraphicsLineItem(
                rect.x(), rect.y() + i * self.section_height,
                rect.x() + rect.width(), rect.y() + i * self.section_height,
                self
            )
            line.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            self.divider_lines.append(line)

    def update_divider_lines(self):
        """Update the position of the divider lines when resizing."""
        rect = self.rect()
        for i, line in enumerate(self.divider_lines, start=1):
            line.setLine(
                rect.x(), rect.y() + i * self.section_height,
                rect.x() + rect.width(), rect.y() + i * self.section_height
            )

    def paint(self, painter: QPainter, option, widget):
        # Draw the rectangle
        super().paint(painter, option, widget)
        # Draw the resize handle
        if self.isSelected():
            painter.setBrush(QBrush(Qt.black))
            painter.drawRect(self.resize_handle_rect)

    def hoverMoveEvent(self, event):
        # Change cursor when hovering over the resize handle
        if self.resize_handle_rect.contains(event.pos()):
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.resize_handle_rect.contains(event.pos()):
            self.resizing = True
            self.previous_mouse_pos = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.resizing:
            delta = event.pos() - self.previous_mouse_pos
            new_rect = self.rect()
            new_rect.setRight(new_rect.right() + delta.x())
            new_rect.setBottom(new_rect.bottom() + delta.y())

            # Ensure minimum size
            min_width = 150
            min_height = 150
            if new_rect.width() < min_width:
                new_rect.setWidth(min_width)
            if new_rect.height() < min_height:
                new_rect.setHeight(min_height)
            self.setRect(new_rect)

            # Update positions and geometry
            self.update_resize_handle()
            self.update_class_name_position()
            self.update_fields_header_position()
            self.update_methods_header_position()
            self.update_fields_position()
            self.update_methods_position()
            self.update_divider_lines()
            self.prepareGeometryChange()
            self.update()
            self.previous_mouse_pos = event.pos()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.resizing:
            self.resizing = False
            self.snap_to_grid()
        else:
            super().mouseReleaseEvent(event)

    def snap_to_grid(self):
        """Snaps the UML class to the nearest grid point."""
        current_pos = self.pos()
        new_x = round(current_pos.x() / self.grid_size) * self.grid_size
        new_y = round(current_pos.y() / self.grid_size) * self.grid_size
        self.setPos(new_x, new_y)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            # Snap to grid while moving
            new_x = round(value.x() / self.grid_size) * self.grid_size
            new_y = round(value.y() / self.grid_size) * self.grid_size
            return QPointF(new_x, new_y)
        return super().itemChange(change, value)

###################################################################################################

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

###################################################################################################

class MainWindow(QMainWindow, Observer):
    def __init__(self, interface):
        super().__init__()
        QWidget.__init__(self)  # Initialize QWidget
        self.interface = interface  # Interface to communicate with UMLCoreManager
        uic.loadUi('prototype_gui.ui', self)
        
        # Create layout and add button
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        
        ############################################################################
        ### MENU BAR ###
        
        # Find "Save As" / "Open" actions
        self.save_button = self.findChild(QAction, "SaveAs")
        self.open_button = self.findChild(QAction, "Open")
        self.label = self.findChild(QLabel, "label")
        
        # Connect the "Save As" action to the click_save_as method
        self.save_button.triggered.connect(self.click_save_as)
        # Connect the "Open" action to the click_save_as method
        self.open_button.triggered.connect(self.click_open)
        
        ############################################################################
        ### TOOLBAR ###
        
        # Find the QAction objects from the toolbar
        self.add_class_action = self.findChild(QAction, "add_class")
        self.delete_class_action = self.findChild(QAction, "delete_class")
        
         # Connect QAction triggered signals to the corresponding methods
        self.add_class_action.triggered.connect(self.add_class_to_diagram)
        self.delete_class_action.triggered.connect(self.delete_selected_class_from_diagram)

        # Create the UML diagram view
        self.uml_view = UMLClassDiagram()
        layout.addWidget(self.uml_view)
        
        ############################################################################
        ### EVENT ###
    def add_class_to_diagram(self):
        # Call the method to add a UML class to the diagram
        self.uml_view.add_class()

    def delete_selected_class_from_diagram(self):
        # Call the method to delete the selected UML class
        self.uml_view.delete_selected_class()

    def reset_diagram_view(self):
        # Call the method to reset the view
        self.uml_view.reset_view()

    # Move the click_save_as function outside the __init__ to make it a class method
    def click_save_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save As", "", "All Files (*);; Python Files (*.py);; JSON Files (*.json)")
        if not file_path:
            return
        self.label.setText(str(file_path))
        filename_with_extension = os.path.basename(file_path)
        filename_without_extension, _ = os.path.splitext(filename_with_extension)
        self.interface.save_gui(filename_without_extension, file_path)
        
    def click_open(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Open", "", "All Files (*);; Python Files (*.py);; JSON Files (*.json)")
        if file_name:
            self.label.setText(str(file_name))

###################################################################################################
