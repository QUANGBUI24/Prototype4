###################################################################################################

import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets, QtGui, QtCore
from UML_VIEW.uml_observer import UMLObserver as Observer

###################################################################################################

class GridWidget(QtWidgets.QWidget):
    """
    GridWidget is a custom widget that displays a grid pattern. This grid can be used
    as a background for applications like UML diagram editors to help align and organize
    graphical elements. It supports zooming in and out using the mouse wheel scroll
    and panning by dragging with the middle mouse button. The cursor changes to a hand
    icon when panning to provide visual feedback.
    """

    def __init__(self, parent=None, grid_size=20, color=QtGui.QColor(200, 200, 200)):
        """
        Initializes the GridWidget instance.

        Parameters:
        - parent (QtWidgets.QWidget, optional): The parent widget. Defaults to None.
        - grid_size (int, optional): The initial spacing between grid lines in pixels. Defaults to 20.
        - color (QtGui.QColor, optional): The color of the grid lines. Defaults to a light gray.
        """
        # Call the superclass (QWidget) constructor to ensure proper initialization
        super().__init__(parent)

        # Store the grid spacing and color as instance variables for later use
        self.grid_size = grid_size
        self.grid_color = color

        # Set the minimum size of the widget to ensure the grid is visible
        self.setMinimumSize(1000, 1000)  # Set a default size; adjust as needed

        # Define minimum and maximum grid sizes to prevent excessive zooming
        self.min_grid_size = 5    # Minimum grid spacing in pixels
        self.max_grid_size = 100  # Maximum grid spacing in pixels

        # Initialize the grid offset to (0, 0), representing no panning
        self.x_offset = 0
        self.y_offset = 0

        # Initialize variables to track panning state
        self.is_panning = False       # Indicates whether panning is currently active
        self.last_mouse_pos = None    # Stores the last mouse position during panning

        # Set the cursor to the default arrow cursor initially
        self.setCursor(QtCore.Qt.ArrowCursor)

    #################################################################
    ### NOT FOR BUTTON EVENT ###
    
    """
    The paintEvent method is a built-in PyQt method that is called whenever the widget needs to be repainted.
    This can occur when the widget is first displayed, resized, or explicitly updated.
    Overriding this method allows for custom drawing on the widget.
    """
    def paintEvent(self, event):
        """
        Handles the painting of the widget. Draws a grid based on the specified grid size, color,
        and current offsets.

        Parameters:
        - event (QtGui.QPaintEvent): The paint event containing information about the region to be repainted.
        """
        # Create a QPainter object to handle the drawing operations
        painter = QtGui.QPainter(self)

        # Enable antialiasing for smoother lines
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Create a QPen object with the specified grid color
        pen = QtGui.QPen(self.grid_color)

        # Set the width of the pen to 1 pixel for fine grid lines
        pen.setWidth(1)

        # Apply the pen to the painter
        painter.setPen(pen)

        # Calculate the adjusted grid size based on the current zoom level
        adjusted_grid_size = self.grid_size

        # Calculate the starting points for vertical and horizontal lines based on the current offset
        start_x = self.x_offset % adjusted_grid_size
        start_y = self.y_offset % adjusted_grid_size

        # Loop through the width of the widget, drawing vertical lines at intervals of adjusted_grid_size
        x = start_x
        while x < self.width():
            painter.drawLine(x, 0, x, self.height())
            x += adjusted_grid_size

        # Loop through the height of the widget, drawing horizontal lines at intervals of adjusted_grid_size
        y = start_y
        while y < self.height():
            painter.drawLine(0, y, self.width(), y)
            y += adjusted_grid_size

        # End the painting process to free up resources
        painter.end()

    """
    Handles mouse wheel events to implement zoom in and out functionality using the mouse wheel scroll.

    Parameters:
    - event (QtGui.QWheelEvent): The wheel event containing information about the scroll.

    Behavior:
    - Scrolling up (positive delta): Zoom in by decreasing the grid_size, making the grid denser.
    - Scrolling down (negative delta): Zoom out by increasing the grid_size, making the grid sparser.
    - Clamps grid_size between min_grid_size and max_grid_size to prevent excessive zooming.
"""
    def wheelEvent(self, event):
        """
        Handles mouse wheel events to implement zoom in and out functionality using the mouse wheel scroll.

        Parameters:
        - event (QtGui.QWheelEvent): The wheel event containing information about the scroll.
        """
        delta = event.angleDelta().y()

        # Define the zoom step size (number of pixels to adjust per scroll)
        zoom_step = 1  # Adjust this value for faster or slower zooming

        if delta > 0:
            # Wheel scrolled up: Zoom in by decreasing the grid_size
            new_grid_size = self.grid_size + zoom_step

            # Ensure the new grid size does not go below the minimum limit
            if new_grid_size <= self.max_grid_size:
                self.grid_size = new_grid_size
                self.update()  # Request a repaint to apply the new grid size
        elif delta < 0:
            # Wheel scrolled down: Zoom out by increasing the grid_size
            new_grid_size = self.grid_size - zoom_step

            # Ensure the new grid size does not exceed the maximum limit
            if new_grid_size >= self.min_grid_size:
                self.grid_size = new_grid_size
                self.update()  # Request a repaint to apply the new grid size

        # Accept the event to indicate it has been handled
        event.accept()
        
    """
    Handles mouse button press events to initiate panning when the middle mouse button is pressed.

    Parameters:
    - event (QtGui.QMouseEvent): The mouse event containing information about the button pressed.
    """
    def mousePressEvent(self, event):
        """
        Handles mouse button press events to initiate panning when the middle mouse button is pressed.

        Parameters:
        - event (QtGui.QMouseEvent): The mouse event containing information about the button pressed.
        """
        # Check if the middle mouse button was pressed
        if event.button() == QtCore.Qt.MiddleButton:
            # Begin panning
            self.is_panning = True

            # Store the position where the panning started
            self.last_mouse_pos = event.pos()

            # Change the cursor to a closed hand to indicate panning
            self.setCursor(QtCore.Qt.ClosedHandCursor)

            # Accept the event to indicate it has been handled
            event.accept()
        else:
            # For other mouse buttons, pass the event to the superclass
            super().mousePressEvent(event)

    """
    Handles mouse move events to update the grid offset when panning is active.

    Parameters:
    - event (QtGui.QMouseEvent): The mouse event containing information about the cursor position.
    """
    def mouseMoveEvent(self, event):
        """
        Handles mouse move events to update the grid offset when panning is active.

        Parameters:
        - event (QtGui.QMouseEvent): The mouse event containing information about the cursor position.
        """
        # Check if panning is currently active
        if self.is_panning and self.last_mouse_pos is not None:
            # Get the current mouse position
            current_pos = event.pos()

            # Calculate the distance moved since the last mouse position
            delta_x = current_pos.x() - self.last_mouse_pos.x()
            delta_y = current_pos.y() - self.last_mouse_pos.y()

            # Update the grid offsets based on the movement
            self.x_offset += delta_x
            self.y_offset += delta_y

            # Store the new mouse position for the next movement
            self.last_mouse_pos = current_pos

            # Request a repaint to update the grid position
            self.update()

            # Accept the event to indicate it has been handled
            event.accept()
        else:
            # If not panning, pass the event to the superclass
            super().mouseMoveEvent(event)

    """
    Handles mouse button release events to end panning when the middle mouse button is released.

    Parameters:
    - event (QtGui.QMouseEvent): The mouse event containing information about the button released.
    """
    def mouseReleaseEvent(self, event):
        """
        Handles mouse button release events to end panning when the middle mouse button is released.

        Parameters:
        - event (QtGui.QMouseEvent): The mouse event containing information about the button released.
        """
        # Check if the middle mouse button was released
        if event.button() == QtCore.Qt.MiddleButton and self.is_panning:
            # End panning
            self.is_panning = False
            self.last_mouse_pos = None

            # Change the cursor back to the default arrow cursor
            self.setCursor(QtCore.Qt.ArrowCursor)

            # Accept the event to indicate it has been handled
            event.accept()
        else:
            # For other mouse buttons, pass the event to the superclass
            super().mouseReleaseEvent(event)

    #################################################################
    ### FOR BUTTON EVENT ###
    """
    The setGridVisible method controls the visibility of the grid widget.
    """
    def setGridVisible(self, visible):
        """
        Controls the visibility of the grid widget.

        Parameters:
        - visible (bool): If True, the grid is shown; if False, it is hidden.
        """
        # Set the visibility of the widget based on the 'visible' parameter
        self.setVisible(visible)

    """
    The setGridColor method updates the color of the grid lines and repaints the widget to reflect the change.
    """
    def setGridColor(self, color):
        """
        Updates the color of the grid lines and repaints the widget to reflect the change.

        Parameters:
        - color (QtGui.QColor): The new color for the grid lines.
        """
        # Update the grid_color instance variable with the new color
        self.grid_color = color

        # Request a repaint of the widget to apply the new color
        self.update()
        
###################################################################################################

class UMLClassItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, width, height, class_name="ClassName", grid_size=20):
        super().__init__(x, y, width, height)
        self.grid_size = grid_size
        self.setFlags(
            QtWidgets.QGraphicsRectItem.ItemIsMovable |
            QtWidgets.QGraphicsRectItem.ItemIsSelectable |
            QtWidgets.QGraphicsRectItem.ItemIsFocusable |
            QtWidgets.QGraphicsRectItem.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        self.setBrush(QtGui.QBrush(QtCore.Qt.white))
        self.setPen(QtGui.QPen(QtCore.Qt.black))

        # Resizing variables
        self.resizing = False
        self.resize_handle_size = 10
        self.update_resize_handle()  # Update the resize handle's position initially
        self.setCursor(QtCore.Qt.ArrowCursor)

        # Section heights
        self.section_height = height // 4

        # Create and update text labels for class name, fields, and methods
        self.class_name_text = QtWidgets.QGraphicsTextItem(class_name, self)
        self.class_name_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)  # Editable
        self.update_class_name_position()

        # Create Fields and Methods headers
        self.fields_header = QtWidgets.QGraphicsTextItem("+Fields:", self)
        self.update_fields_header_position()

        self.methods_header = QtWidgets.QGraphicsTextItem("+Methods:", self)
        self.update_methods_header_position()

        # Divider lines between sections
        self.divider_lines = []
        self.add_divider_lines()

        # Lists to store fields and methods
        self.fields = []
        self.methods = []

    def mouseDoubleClickEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        """Detects double-click events to add a field or method."""
        # Check where the double-click happened relative to the bounding rect
        pos = event.pos()
        rect = self.rect()

        # Determine if the click was in the fields section
        if rect.y() + self.section_height < pos.y() < rect.y() + 2 * self.section_height:
            # Double-click in Fields section
            text, ok = QtWidgets.QInputDialog.getText(None, "Add Field", "Enter field name:")
            if ok and text:
                self.add_field(text)

        # Determine if the click was in the methods section
        elif rect.y() + 2 * self.section_height < pos.y() < rect.y() + 3 * self.section_height:
            # Double-click in Methods section
            text, ok = QtWidgets.QInputDialog.getText(None, "Add Method", "Enter method name:")
            if ok and text:
                self.add_method(text)

        super().mouseDoubleClickEvent(event)

    def add_field(self, field_name="Field1"):
        """Adds a new field to the fields section and resizes the class box."""
        new_field = QtWidgets.QGraphicsTextItem(f"  - {field_name}", self)
        new_field.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)  # Make text editable
        self.fields.append(new_field)
        self.update_fields_position()
        self.adjust_height()

    def add_method(self, method_name="Method1"):
        """Adds a new method to the methods section and resizes the class box."""
        new_method = QtWidgets.QGraphicsTextItem(f"  - {method_name}:", self)
        new_method.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)  # Make text editable
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
        self.resize_handle_rect = QtCore.QRectF(
            rect.right() - self.resize_handle_size,
            rect.bottom() - self.resize_handle_size,
            self.resize_handle_size,
            self.resize_handle_size
        )

    def add_divider_lines(self):
        """Add horizontal divider lines to separate sections."""
        rect = self.rect()
        for i in range(1, 4):
            line = QtWidgets.QGraphicsLineItem(
                rect.x(), rect.y() + i * self.section_height,
                rect.x() + rect.width(), rect.y() + i * self.section_height,
                self
            )
            line.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
            self.divider_lines.append(line)

    def update_divider_lines(self):
        """Update the position of the divider lines when resizing."""
        rect = self.rect()
        for i, line in enumerate(self.divider_lines, start=1):
            line.setLine(
                rect.x(), rect.y() + i * self.section_height,
                rect.x() + rect.width(), rect.y() + i * self.section_height
            )

    def paint(self, painter: QtGui.QPainter, option, widget):
        # Draw the rectangle
        super().paint(painter, option, widget)
        # Draw the resize handle
        if self.isSelected():
            painter.setBrush(QtGui.QBrush(QtCore.Qt.black))
            painter.drawRect(self.resize_handle_rect)

    def hoverMoveEvent(self, event):
        # Change cursor when hovering over the resize handle
        if self.resize_handle_rect.contains(event.pos()):
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.resize_handle_rect.contains(event.pos()):
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
        if change == QtWidgets.QGraphicsItem.ItemPositionChange and self.scene():
            # Snap to grid while moving
            new_x = round(value.x() / self.grid_size) * self.grid_size
            new_y = round(value.y() / self.grid_size) * self.grid_size
            return QtCore.QPointF(new_x, new_y)
        return super().itemChange(change, value)

###################################################################################################

class UMLClassDiagram(QtWidgets.QGraphicsView):
    def __init__(self):
        super().__init__()

        # Set up the scene with a large initial size
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

        # Enable scrollbars to appear when needed
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

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
        pen = QtGui.QPen(QtCore.Qt.lightGray)
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

class MainWindow(QtWidgets.QMainWindow, Observer):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface  # Interface to communicate with UMLCoreManager

        # Load the UI first to access all elements defined in the UI file
        uic.loadUi('prototype_gui.ui', self)

        # Create the grid widget and set it as the central widget of the main window
        self.grid_widget = GridWidget(self)
        self.setCentralWidget(self.grid_widget)
        layout = QtWidgets.QVBoxLayout(self.grid_widget)
        
        # Create the UML diagram view
        self.uml_view = UMLClassDiagram()
        layout.addWidget(self.uml_view)

        #################################################################   
        ### BUTTONS ###
        
        ## GRID BUTTONS ##
        # Find the QAction objects from the UI file
        self.toggle_grid_button = self.findChild(QtWidgets.QAction, "toggle_grid")
        self.change_grid_color_button = self.findChild(QtWidgets.QAction, "change_grid_color")
        # Connect QAction signals to the respective slot methods
        # The 'toggled' signal emits a boolean value indicating the checked state
        self.toggle_grid_button.triggered.connect(self.toggle_grid_method)
        # Connect the change grid color action to the respective slot method
        self.change_grid_color_button.triggered.connect(self.change_gridColor_method)
        
        ## UML DIAGRAM BUTTONS ##
        # Find the QAction objects from the toolbar
        self.add_class_action = self.findChild(QtWidgets.QAction, "add_class")
        self.add_class_action.triggered.connect(self.add_class_to_diagram)
        self.delete_class_action = self.findChild(QtWidgets.QAction, "delete_class")
        self.delete_class_action.triggered.connect(self.delete_selected_class_from_diagram)
         
    #################################################################    
    ### EVENT FUNCTIONS ###
    
    ## GRID EVENTS ##

    """
        Toggles the visibility of the grid widget each time the toggle button is clicked.
        If the grid is visible, it will be hidden, and vice versa.

        Parameters:
        - checked (bool): Indicates whether the grid should be visible.
    """
    def toggle_grid_method(self, checked):
        # Set the visibility of the grid widget based on the checked state
        self.grid_widget.setGridVisible(checked)

    """
    Opens a color dialog to allow the user to select a new grid color for the grid widget.
    """
    def change_gridColor_method(self):
        # Open a color dialog with the current grid color as the initial color
        color = QtWidgets.QColorDialog.getColor(initial=self.grid_widget.grid_color, parent=self, title="Select Grid Color")
        # If the user selected a valid color, update the grid color
        if color.isValid():
            self.grid_widget.setGridColor(color)
            
    """
    Adds a new UML class item to the scene when the 'add_class' QAction is triggered.
    """       
    def add_class_to_diagram(self):
        # Call the method to add a UML class to the diagram
        self.uml_view.add_class()
        
    def delete_selected_class_from_diagram(self):
        # Call the method to delete the selected UML class
        self.uml_view.delete_selected_class()

    #################################################################



