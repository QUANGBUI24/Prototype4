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
    
    Parameters:
        - parent (QtWidgets.QWidget, optional): The parent widget. Defaults to None.
        - grid_size (int, optional): The initial spacing between grid lines in pixels. Defaults to 20.
        - color (QtGui.QColor, optional): The color of the grid lines. Defaults to a light gray.
    """

    def __init__(self, parent=None, grid_size=20, color=QtGui.QColor(200, 200, 200)):
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
    
    Parameters:
        - event (QtGui.QPaintEvent): The paint event containing information about the region to be repainted.
    """
    def paintEvent(self, event):
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
    
    Parameters:
        - event (QtGui.QWheelEvent): The wheel event containing information about the scroll.
"""
    def wheelEvent(self, event):
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
    
    Parameters:
        - visible (bool): If True, the grid is shown; if False, it is hidden.
    """
    def setGridVisible(self, visible):
        # Set the visibility of the widget based on the 'visible' parameter
        self.setVisible(visible)

    """
    The setGridColor method updates the color of the grid lines and repaints the widget to reflect the change.
    
    Parameters:
        - color (QtGui.QColor): The new color for the grid lines.
    """
    def setGridColor(self, color):
        # Update the grid_color instance variable with the new color
        self.grid_color = color

        # Request a repaint of the widget to apply the new color
        self.update()

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
        # self.add_class_action = self.findChild(QtWidgets.QAction, "add_class")
        # self.add_class_action.triggered.connect(self.add_class_to_diagram)
        # self.delete_class_action = self.findChild(QtWidgets.QAction, "delete_class")
        # self.delete_class_action.triggered.connect(self.delete_selected_class_from_diagram)
         
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
    # def add_class_to_diagram(self):
    #     # Call the method to add a UML class to the diagram
    #     self.uml_view.add_class()
        
    # def delete_selected_class_from_diagram(self):
    #     # Call the method to delete the selected UML class
    #     self.uml_view.delete_selected_class()

    #################################################################



