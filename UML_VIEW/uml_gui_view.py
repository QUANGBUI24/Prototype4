###################################################################################################

import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets, QtGui, QtCore
from UML_VIEW.uml_observer import UMLObserver as Observer

###################################################################################################

class UMLClassBox(QtWidgets.QGraphicsRectItem):
    """
    A representation of a UML class box with editable sections.
    """
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

        # Create labels for attributes (Fields) and methods
        self.fields_label = QtWidgets.QGraphicsTextItem(self)
        self.fields_label.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.fields_label.setPlainText("Fields")  # Set fields label text

        self.methods_label = QtWidgets.QGraphicsTextItem(self)
        self.methods_label.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.methods_label.setPlainText("Methods")  # Set methods label text

        # Create text items for attributes and methods
        self.attributes_text = QtWidgets.QGraphicsTextItem(self)
        self.attributes_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.attributes_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.attributes_text.setPlainText("\n".join(self.attributes))  # Set attributes text

        self.methods_text = QtWidgets.QGraphicsTextItem(self)
        self.methods_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.methods_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.methods_text.setPlainText("\n".join(self.methods))  # Set methods text

        # Resizing attributes
        self.is_box_dragged = False
        self.is_resizing = False
        self.current_handle = None
        self.handle_size = 12  # Size of the corner handles
        self.create_resize_handles()

        # Update positions based on the current box size
        self.update_positions()

    def create_resize_handles(self):
        """Create four resize handles at the corners of the class box."""
        # Create four handles for each corner
        self.handles = {
            'bottom_right': QtWidgets.QGraphicsEllipseItem(0, 0, self.handle_size, self.handle_size, self)
        }

        for handle in self.handles.values():
            handle.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))  # Red color for visibility
            handle.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)  # Enable update on move/resize
            handle.setAcceptHoverEvents(True)  # Allow hover events on handles
            handle.hoverEnterEvent = self.handle_hoverEnterEvent
            handle.hoverLeaveEvent = self.handle_hoverLeaveEvent

    def update_positions(self):
        """Update the positions of text items and handles based on the current box size."""
        rect = self.rect()

        # Set positions relative to the box size
        self.class_name_text.setPos(rect.x() + 5, rect.y() + 5)
        self.fields_label.setPos(rect.x() + 5, rect.y() + 35)
        self.methods_label.setPos(rect.x() + 5, rect.y() + 120)
        self.attributes_text.setPos(rect.x() + 15, rect.y() + 55)
        self.methods_text.setPos(rect.x() + 15, rect.y() + 140)

        # Position the resize handles
        self.handles['bottom_right'].setPos(rect.x() + rect.width() - self.handle_size // 2, rect.y() + rect.height() - self.handle_size // 2)  # Bottom-right

        # Create and position separator lines based on the current box size
        if hasattr(self, 'separator_line1'):
            self.separator_line1.setLine(0, 30, rect.width(), 30)  # Line below class name
            self.separator_line2.setLine(0, 115, rect.width(), 115)  # Line below attributes
        else:
            self.separator_line1 = QtWidgets.QGraphicsLineItem(0, 30, rect.width(), 30, self)  # Line below class name
            self.separator_line2 = QtWidgets.QGraphicsLineItem(0, 115, rect.width(), 115, self)  # Line below attributes

            self.separator_line1.setPen(QtGui.QPen(QtCore.Qt.black))  # Set line color
            self.separator_line2.setPen(QtGui.QPen(QtCore.Qt.black))  # Set line color
        
    def handle_hoverEnterEvent(self, event):
        """Change cursor to resize when hovering over this handle."""
        self.setCursor(QtCore.Qt.SizeFDiagCursor)  # Example cursor change for handles
        event.accept()

    def handle_hoverLeaveEvent(self, event):
        """Reset cursor when leaving this handle."""
        self.setCursor(QtCore.Qt.ArrowCursor)  # Reset cursor to default
        event.accept()
        
    def mousePressEvent(self, event):
        """Handle mouse press events for the UML class box or the handles."""
        if event.button() == QtCore.Qt.LeftButton:
            if self.isUnderMouse() and not any(handle.isUnderMouse() for handle in self.handles.values()):
                self.is_box_dragged = True  # Set flag for box dragging
            elif any(handle.isUnderMouse() for handle in self.handles.values()):
                # Determine which handle is being pressed
                for handle_name, handle in self.handles.items():
                    if handle.isUnderMouse():
                        self.current_handle = handle_name  # Store the name of the handle
                        self.is_resizing = True  # Set flag for resizing
                        break
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move events for dragging or resizing."""
        if self.is_resizing and self.current_handle is not None:
            new_rect = self.rect()

            # Get the new width and height based on the mouse position
            new_width = event.pos().x() - new_rect.x()
            new_height = event.pos().y() - new_rect.y()

            # Calculate minimum height based on the text items
            min_height = (self.fields_label.y() + self.fields_label.boundingRect().height() +
                        self.attributes_text.boundingRect().height() +
                        self.methods_label.boundingRect().height() +
                        self.methods_text.boundingRect().height() + 40)  # Add padding

            # Calculate the maximum width based on the longest string in the labels and text items
            longest_string_width = max(
                self.class_name_text.boundingRect().width(),
                self.fields_label.boundingRect().width(),
                self.attributes_text.boundingRect().width(),
                self.methods_label.boundingRect().width(),
                self.methods_text.boundingRect().width()
            ) + 20  # Add some padding

            # Ensure the box does not overlap with text
            if new_width >= longest_string_width:
                new_rect.setWidth(new_width)

            if new_height >= min_height:
                new_rect.setHeight(new_height)

            # Set the new rectangle size
            self.setRect(new_rect)
            self.update_positions()
        else:
            super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        """Override the mouse release event to stop dragging or resizing and snap the UML class box to the nearest grid position."""
        if self.is_box_dragged:
            self.snap_to_grid()  # Move the box with the mouse
            event.accept()
            self.is_box_dragged = False  # Reset dragging flag
        elif self.is_resizing:
            self.is_resizing = False  # Reset resizing flag
            self.current_handle = None  # Reset current handle

        super().mouseReleaseEvent(event)

    def snap_to_grid(self):
        """Snap the UML class box to the nearest grid position."""
        grid_size = 20  # Define your grid size here (should match the one in GridGraphicsView)
        pos = self.pos()

        # Snap x-coordinate
        new_x = round(pos.x() / grid_size) * grid_size
        # Snap y-coordinate
        new_y = round(pos.y() / grid_size) * grid_size
        
        # Set the new position
        self.setPos(new_x, new_y)

        # Optionally, update the positions of other elements after snapping
        self.update_positions()

###################################################################################################

class GridGraphicsView(QtWidgets.QGraphicsView):
    """
    GridGraphicsView is a custom view that displays a grid pattern. This grid can be used
    as a background for applications like UML diagram editors to help align and organize
    graphical elements. It supports zooming in and out using the mouse wheel scroll
    and panning by dragging with the middle mouse button. The cursor changes to a hand
    icon when panning to provide visual feedback.
    """

    def __init__(self, parent=None, grid_size=20, color=QtGui.QColor(200, 200, 200)):
        """
        Initializes the GridGraphicsView instance.

        Parameters:
        - parent (QtWidgets.QWidget, optional): The parent widget. Defaults to None.
        - grid_size (int, optional): The initial spacing between grid lines in pixels. Defaults to 20.
        - color (QtGui.QColor, optional): The color of the grid lines. Defaults to a light gray.
        """
        # Set up the scene and view
        self.scene = QtWidgets.QGraphicsScene(parent)
        super().__init__(self.scene, parent)
        
        # Initialize grid visibility attribute
        self.grid_visible = True  # Default to visible
        
        # Set initial mode (light mode by default)
        self.is_dark_mode = False
        self.setLightMode()
        
        # Define the zoom step size (number of pixels to adjust per scroll)
        self.zoom_step = 2  # Adjust this value for faster or slower zooming
        
        # Store the grid properties
        self.grid_size = grid_size
        self.grid_color = color

        # Define minimum and maximum grid sizes to prevent excessive zooming
        self.min_grid_size = 20    # Minimum grid spacing in pixels
        self.max_grid_size = 100  # Maximum grid spacing in pixels

        # Set initial view properties
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setSceneRect(-5000, -5000, 10000, 10000)  # Set large scene to ensure sufficient space for the grid
        self.setScene(self.scene)
        
        # Enable panning state variables
        self.is_panning = False
        self.last_mouse_pos = None
        
        # Track the selected UML class item
        self.selected_class = None  
        
    def add_class(self):
        # Add a sample UML class box to the scene
        class_box = UMLClassBox("ClassName", ["Field_1", "Field_2"], ["Method_1()", "Method_2()"])
        class_box.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)  # Make the box movable
        class_box.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)  # Make the box selectable
        class_box.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)  # Enable update on move/resize
        self.scene.addItem(class_box)
        
    def delete_selected_class(self):
        """Deletes the selected class from the scene."""
        if self.selected_class:
            self.scene.removeItem(self.selected_class)
            self.selected_class = None

    def drawBackground(self, painter, rect):
        """
        Draws the background grid pattern.

        Parameters:
        - painter (QtGui.QPainter): The painter object used for custom painting.
        - rect (QtCore.QRectF): The area to be painted.
        """
        # Fill the background with the current background color
        if self.is_dark_mode:
            painter.fillRect(rect, QtGui.QColor(30, 30, 30))  # Dark background
        else:
            painter.fillRect(rect, QtGui.QColor(255, 255, 255))  # Light background
            
        if self.grid_visible:  # Check if the grid should be drawn
            # Create a QPen object with the specified grid color
            pen = QtGui.QPen(self.grid_color)
            pen.setWidth(1)

            # Set the painter to use the pen
            painter.setPen(pen)

            # Calculate the top-left and bottom-right points of the rect
            left = int(rect.left()) - (int(rect.left()) % self.grid_size)
            top = int(rect.top()) - (int(rect.top()) % self.grid_size)

            # Draw vertical lines across the scene
            for x in range(left, int(rect.right()), self.grid_size):
                painter.drawLine(x, int(rect.top()), x, int(rect.bottom()))

            # Draw horizontal lines across the scene
            for y in range(top, int(rect.bottom()), self.grid_size):
                painter.drawLine(int(rect.left()), y, int(rect.right()), y)
            
    def setLightMode(self):
        """
        Sets the view to light mode.
        """
        self.grid_color = QtGui.QColor(200, 200, 200)  # Light gray for grid lines
        self.is_dark_mode = False
        self.viewport().update()
        self.scene.update()

    def setDarkMode(self):
        """
        Sets the view to dark mode.
        """
        self.grid_color = QtGui.QColor(0,255,255)  # Cyan for grid lines
        self.is_dark_mode = True
        self.viewport().update()
        self.scene.update()

    def toggleMode(self):
        """
        Toggles between dark mode and light mode.
        """
        if self.is_dark_mode:
            self.setLightMode()
        else:
            self.setDarkMode()

    def wheelEvent(self, event):
        """
        Handles mouse wheel events to implement zoom in and out functionality using the mouse wheel scroll.

        Parameters:
        - event (QtGui.QWheelEvent): The wheel event containing information about the scroll.
        """
        delta = event.angleDelta().y()
        
        if delta > 0:
            # Wheel scrolled up: Zoom in by decreasing the grid_size
            new_grid_size = self.grid_size + self.zoom_step

            # Ensure the new grid size does not go below the minimum limit
            if new_grid_size <= self.max_grid_size:
                self.grid_size = new_grid_size
                self.viewport().update()  # Request a repaint to apply the new grid size
        elif delta < 0:
            # Wheel scrolled down: Zoom out by increasing the grid_size
            new_grid_size = self.grid_size - self.zoom_step

            # Ensure the new grid size does not exceed the maximum limit
            if new_grid_size >= self.min_grid_size:
                self.grid_size = new_grid_size
                self.viewport().update()  # Request a repaint to apply the new grid size
        
        # Accept the event to indicate it has been handled
        event.accept()

    def mousePressEvent(self, event):
        """
        Handles mouse button press events to initiate panning when the middle mouse button is pressed.

        Parameters:
        - event (QtGui.QMouseEvent): The mouse event containing information about the button pressed.
        """
        # Tracking chosen class box
        item = self.itemAt(event.pos())
        if isinstance(item, UMLClassBox):
            self.selected_class = item
        else:
            self.selected_class = None
            
        # Dragging around the grid view using middle mouse button
        if event.button() == QtCore.Qt.MiddleButton:
            # Start panning
            self.is_panning = True
            self.last_mouse_pos = event.pos()
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Handles mouse move events to update the scene position when panning is active.

        Parameters:
        - event (QtGui.QMouseEvent): The mouse event containing information about the cursor position.
        """
        if self.is_panning and self.last_mouse_pos is not None:
            # Calculate the distance moved
            delta = event.pos() - self.last_mouse_pos

            # Translate the view accordingly
            self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
            self.translate(delta.x(), delta.y())

            # Update last mouse position
            self.last_mouse_pos = event.pos()

            # Accept the event to indicate it has been handled
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Handles mouse button release events to end panning when the middle mouse button is released.

        Parameters:
        - event (QtGui.QMouseEvent): The mouse event containing information about the button released.
        """
        if event.button() == QtCore.Qt.MiddleButton and self.is_panning:
            # End panning
            self.is_panning = False
            self.last_mouse_pos = None
            self.setCursor(QtCore.Qt.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def setGridVisible(self, visible):
        """
        Controls the visibility of the grid lines in the scene.

        Parameters:
        - visible (bool): If True, the grid is shown; if False, it is hidden.
        """
        self.grid_visible = visible  # Store visibility state
        self.viewport().update()  # Redraw the view

    def setGridColor(self, color):
        """
        Updates the color of the grid lines and repaints the scene to reflect the change.

        Parameters:
        - color (QtGui.QColor): The new color for the grid lines.
        """
        self.grid_color = color
        self.viewport().update()  # Redraw the grid with the new color
    
    def resetView(self):
        """Resets the zoom and position to the initial state."""
        self.grid_size = 20
        self.resetTransform()  # Reset the zoom to its original state
        self.centerOn(0, 0)  # Center the view on the origin (initial position)

###################################################################################################

class MainWindow(QtWidgets.QMainWindow, Observer):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface  # Interface to communicate with UMLCoreManager

        # Load the UI first to access all elements defined in the UI file
        uic.loadUi('prototype_gui.ui', self)

        # Create the grid widget and set it as the central widget of the main window
        # self.grid_view = GridWidget(self)
        self.grid_view = GridGraphicsView()
        self.setCentralWidget(self.grid_view)
        self.box = UMLClassBox()

        #################################################################   
        ### BUTTONS ###
        
        ## GRID/VIEW BUTTONS ##
        # Find the QAction objects from the UI file
        self.toggle_grid_button = self.findChild(QtWidgets.QAction, "toggle_grid")
        self.change_grid_color_button = self.findChild(QtWidgets.QAction, "change_grid_color")
        self.reset_view_button = self.findChild(QtWidgets.QAction, "reset_view")
        self.toggle_mode_button = self.findChild(QtWidgets.QAction, "toggle_mode")
        
        # Connect QAction signals to the respective slot methods
        # The 'toggled' signal emits a boolean value indicating the checked state
        self.toggle_grid_button.triggered.connect(self.toggle_grid_method)
        self.change_grid_color_button.triggered.connect(self.change_gridColor_method)
        self.reset_view_button.triggered.connect(self.reset_view_method)
        self.toggle_mode_button.triggered.connect(self.toggle_mode_method)
        
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
        self.grid_view.setGridVisible(checked)

    """
    Opens a color dialog to allow the user to select a new grid color for the grid widget.
    """
    def change_gridColor_method(self):
        # Open a color dialog with the current grid color as the initial color
        color = QtWidgets.QColorDialog.getColor(initial=self.grid_view.grid_color, parent=self, title="Select Grid Color")
        # If the user selected a valid color, update the grid color
        if color.isValid():
            self.grid_view.setGridColor(color)
            
    """
    Helps user to get to default screen
    """      
    def reset_view_method(self):
        # Reset to original view
        self.grid_view.resetView()
        
    """
    Switching light and dark mode
    """       
    def toggle_mode_method(self):
        self.grid_view.toggleMode()
            
    """
    Adds a new UML class item to the scene when the 'add_class' QAction is triggered.
    """       
    def add_class_to_diagram(self):
        # Call the method to add a UML class to the diagram
        self.grid_view.add_class()
        
    def delete_selected_class_from_diagram(self):
        # Call the method to delete the selected UML class
        self.grid_view.delete_selected_class()

    #################################################################



