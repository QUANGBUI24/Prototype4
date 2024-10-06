###################################################################################################

import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets, QtGui, QtCore
from UML_VIEW.uml_observer import UMLObserver as Observer
  
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
        self.setVisible(visible)

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

class UMLClassBox(QtWidgets.QGraphicsRectItem):
    pass

###################################################################################################

class MainWindow(QtWidgets.QMainWindow, Observer):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface  # Interface to communicate with UMLCoreManager

        # Load the UI first to access all elements defined in the UI file
        uic.loadUi('prototype_gui.ui', self)

        # Create the grid widget and set it as the central widget of the main window
        # self.grid_widget = GridWidget(self)
        self.grid_widget = GridGraphicsView()
        self.setCentralWidget(self.grid_widget)

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
    Helps user to get to default screen
    """      
    def reset_view_method(self):
        # Reset to original view
        self.grid_widget.resetView()
        
    """
    Switching light and dark mode
    """       
    def toggle_mode_method(self):
        self.grid_widget.toggleMode()
            
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



