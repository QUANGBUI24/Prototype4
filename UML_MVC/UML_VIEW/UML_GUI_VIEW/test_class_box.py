import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from functools import partial

###################################################################################################
# ADD ROOT PATH #
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.append(root_path)

from UML_ENUM_CLASS.uml_enum import BoxDefaultStat as Default
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_editable_text_item import UMLEditableTextItem as Text

###################################################################################################

class UMLTestBox(QtWidgets.QGraphicsRectItem):
    """
    UMLTestBox represents a resizable, movable UML class box in a UML diagram.
    It contains attributes like class name, fields, methods, parameters, 
    and provides handles for resizing the box.
    """
    def __init__(self, interface, class_name="ClassName", field_list=None, method_list=None, parameter_list=None, parent=None):
        """
        Initialize the UMLTestBox with default settings, including the class name, fields, methods, and handles.
        
        Args:
            interface: The interface for communication with UML components.
            class_name (str): The initial name of the class. Defaults to "ClassName".
            field_list (list): A list of fields for the class. Defaults to an empty list if not provided.
            method_list (list): A list of methods for the class. Defaults to an empty list if not provided.
            parameter_list (list): A list of parameters for the methods. Defaults to an empty list if not provided.
            parent: The parent item, usually a QGraphicsScene. Defaults to None.
        """
        #################################################################
        # Calling constructor from parent class
        super().__init__(parent)

        # Interface to communicate with UMLInterface
        self.interface = interface

        #################################################################
        ### FIELD, METHOD, PARAMETER, HANDLE AND CONNECT POINT LIST ###
        # Initialize lists for fields, methods, parameters, and resize handles.
        self.field_list = field_list if field_list is not None else []
        self.method_list = method_list if method_list is not None else []
        self.parameter_list = parameter_list if parameter_list is not None else []
        self.handles_list = []
        self.connection_points_list = []

        #################################################################
        ### UML CLASS BOX DEFAULT SETUP ###
        
        # Default position, dimensions, handle (for resize), and connect points for the class box.
        self.default_box_x = Default.BOX_DEFAULT_X.value
        self.default_box_y = Default.BOX_DEFAULT_Y.value
        self.default_box_width = Default.BOX_DEFAULT_WIDTH.value
        self.default_box_height = Default.BOX_DEFAULT_HEIGHT.value
        self.default_margin = Default.BOX_DEFAULT_MARGIN.value
        # Handle points and connection points size
        self.handle_size = 10
        self.connection_point_size = 6
        # Initialize resizing and connection properties
        self.is_box_dragged = False
        self.is_resizing = False
        self.current_handle = None

        #################################
        
        # Define bounding rectangle of the class box
        self.setRect(self.default_box_x, self.default_box_y, self.default_box_width, self.default_box_height)
        # Set border color (black)
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))  
        # Set background color (cyan)
        self.setBrush(QtGui.QBrush(QtGui.QColor(0,191,255)))  
        # Set class box selectable
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        # Set class box movable
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True) 
        # Enable the box to send geometry change events.
        # This allows the box to notify the parent item (the class box) when it moves or is resized.
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        # Enable hover events
        self.setAcceptHoverEvents(True)
        
        #################################
        
        # Class name text box and make it appear at the center of the box.
        self.class_name_text = self.create_text_item(class_name, editable=True)
        # Connect the text change callback to ensure it re-centers when the text changes.
        self.class_name_text.document().contentsChanged.connect(self.centering_class_name)
        # Centering class name initially.
        self.centering_class_name()
        # Create handles for resizing the class box.
        self.create_resize_handles()
        # Create connection point for arrow line.
        self.create_connection_points()

        #################################

    #################################################################
    ### MEMBER FUNCTIONS ###
    
    ## UPDATE BOX AND IS COMPONENTS ##
    
    def update_box(self,):
        # Set positions of text items relative to each other #
        self.centering_class_name()
        # Update handles
        self.update_handle_positions()
        # Update connection points
        self.update_connection_point_positions()
    
    def create_resize_handles(self):
        """
        Create four resize handles at the corners of the UML box.
        These handles will be used to resize the UML box by dragging.
        Each QGraphicsEllipseItem(self) creates an ellipse 
        (a small circular handle) and links it to the current object (self), which is the UML box.
        """
        self.handles_list = {
            'top_left': QtWidgets.QGraphicsEllipseItem(self),
            'top_right': QtWidgets.QGraphicsEllipseItem(self),
            'bottom_left': QtWidgets.QGraphicsEllipseItem(self),
            'bottom_right': QtWidgets.QGraphicsEllipseItem(self),
        }

        for handle_name, handle in self.handles_list.items():
            # Set handle size and position based on the size of the box
            handle.setRect(-self.handle_size / 2, -self.handle_size / 2, self.handle_size, self.handle_size)

            # Set the appearance of the handle
            handle.setPen(QtGui.QPen(QtGui.QColor(0,0,0)))  # Black border
            handle.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))  # White fill

            # Set the handle to be non-movable and send geometry changes to the parent
            handle.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            handle.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

            # Allow hover events to change the cursor during interaction
            handle.setAcceptHoverEvents(True)

            # Set hover events to trigger custom cursor change for each handle
            handle.hoverEnterEvent = partial(self.handle_hoverEnterEvent, handle_name=handle_name)
            handle.hoverLeaveEvent = self.handle_hoverLeaveEvent

        # Initial handle positions based on the current size of the box
        self.update_handle_positions()

    def create_connection_points(self):
        """
        Create four connection points (top, bottom, left, right) for linking arrows between UML boxes.
        Each connection point is represented by a small ellipse at the edge of the UML box.
        """
        self.connection_points_list = {
            'top': QtWidgets.QGraphicsEllipseItem(self),
            'bottom': QtWidgets.QGraphicsEllipseItem(self),
            'left': QtWidgets.QGraphicsEllipseItem(self),
            'right': QtWidgets.QGraphicsEllipseItem(self),
        }

        # point_name will be used later for 
        for point_name, cp_item in self.connection_points_list.items():
            # Set the size and position of the connection point
            cp_item.setRect(-5, -5, self.connection_point_size, self.connection_point_size)

            # Set the appearance of the connection point
            cp_item.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))  # Black color fill
            cp_item.setPen(QtGui.QPen(QtCore.Qt.black))  # Black border

            # Disable movement and selection of connection points
            cp_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            cp_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)

        # Update the positions of the connection points based on the size of the box
        self.update_connection_point_positions()

    def update_handle_positions(self):
        """
        Update the positions of the resize handles based on the current size of the UML box.
        This ensures the handles remain at the corners of the box.
        """
        rect = self.rect()
        self.handles_list['top_left'].setPos(rect.topLeft())
        self.handles_list['top_right'].setPos(rect.topRight())
        self.handles_list['bottom_left'].setPos(rect.bottomLeft())
        self.handles_list['bottom_right'].setPos(rect.bottomRight())

    def update_connection_point_positions(self):
        """
        Update the positions of the connection points based on the size of the UML box.
        Connection points are positioned at the center of the edges (top, bottom, left, right).
        """
        rect = self.rect()
        self.connection_points_list['top'].setPos(rect.center().x(), rect.top())
        self.connection_points_list['bottom'].setPos(rect.center().x(), rect.bottom())
        self.connection_points_list['left'].setPos(rect.left(), rect.center().y())
        self.connection_points_list['right'].setPos(rect.right(), rect.center().y())

    #################################
    ## CLASS NAME TEXT RELATED ##
    
    def create_text_item(self, text:str, editable=False, is_field=None, is_method=None, is_parameter=None):
        """
        Create and return a QGraphicsTextItem with editing capabilities.

        Parameters:
        - text (str): The initial text of the item.
        - change_callback (function): Optional function to call when text content changes.
        - editable (bool): Whether the text item is editable.

        Returns:
        - EditableTextItem: The created text item.
        """
        text_item = Text(text=text, parent=self)  # Use the custom EditableTextItem
        if editable:
            text_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
            text_item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        return text_item
    
    def centering_class_name(self):
        """
        Centers the class name text inside the UML class box horizontally.

        This function calculates the position of the class name text based on the width of the UML class box 
        and the width of the text. It adjusts the position of the text so that it is horizontally centered 
        within the class box. The vertical position is fixed using a default margin.

        Steps:
        1. Retrieve the width of the UML class box using self.rect().
        2. Calculate the width of the class name text using self.class_name_text.boundingRect().width().
        3. Compute the new x-position for the class name by centering it within the box.
        4. Set the new position for the class name text at the calculated x-position, with the y-position 
        remaining fixed at the default margin.

        Parameters:
        None
        """
        # Get the current width of the UML class box
        box_width = self.rect().width()

        # Get the width of the class name text using its bounding rectangle
        class_name_width = self.class_name_text.boundingRect().width()

        # Calculate the x-position to center the class name horizontally
        class_name_x_pos = self.rect().topLeft().x() + (box_width - class_name_width) / 2

        # Set the class name's position at the top, ensuring it stays horizontally centered
        # The y-position remains fixed at a margin from the top
        self.class_name_text.setPos(class_name_x_pos, self.rect().topLeft().y() + self.default_margin)
    
    #################################
    ## MOUSE EVENT RELATED ##

    def handle_hoverEnterEvent(self, event, handle_name):
        """
        Change cursor to resize when hovering over the resize handle.
    
        Parameters:
        - event (QGraphicsSceneHoverEvent): The hover event.
        - handle_name (str): The name of the handle that is hovered over (top_left, top_right, bottom_left, bottom_right).
        """ 
        # Change the cursor based on which handle is being hovered
        if handle_name == 'top_left' or handle_name == 'bottom_right':
            self.setCursor(QtCore.Qt.SizeFDiagCursor)  # Backward diagonal resize cursor
        elif handle_name == 'top_right' or handle_name == 'bottom_left':
            self.setCursor(QtCore.Qt.SizeBDiagCursor)  # Forward diagonal resize cursor
        event.accept()
        
    def handle_hoverLeaveEvent(self, event):
        """
        Reset cursor when leaving the resize handle.

        Parameters:
        - event (QGraphicsSceneHoverEvent): The hover event.
        """
        self.setCursor(QtCore.Qt.ArrowCursor)  # Reset cursor to default arrow
        event.accept()
            
    def mousePressEvent(self, event):
        """
        Handle mouse press events for dragging or resizing.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        if event.button() == QtCore.Qt.LeftButton:
            if self.isUnderMouse() and not any(
                handle.isUnderMouse() for handle in self.handles_list.values()
            ):
                self.is_box_dragged = True  # Start dragging the box
            elif any(handle.isUnderMouse() for handle in self.handles_list.values()):
                # Determine which handle is being pressed for resizing
                for handle_name, handle in self.handles_list.items():
                    if handle.isUnderMouse():
                        self.current_handle = handle_name
                        self.is_resizing = True
                        break
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """
        Handle the mouse movement event for resizing the UML box.

        This function updates the size of the UML box based on the handle being dragged during resizing. 
        It ensures that the box maintains a minimum width and height based on the longest string (class name)
        to prevent content from being cut off. The handle being dragged determines which part of the box 
        (top-left, top-right, bottom-left, or bottom-right) is adjusted. The new dimensions are calculated 
        based on the mouse position, and the box is updated accordingly.

        Parameters:
            event (QGraphicsSceneMouseEvent): The event that provides the mouse movement data.
        """
        
        # Check if the box is being resized and if a specific handle is active
        if self.is_resizing and self.current_handle:
            new_rect = self.rect()  # Get the current rectangle (box) dimensions
            # self.mapFromScene(): Converts the mouse’s global position to the local coordinate system of the UML box. 
            # This ensures that resizing is accurate relative to the box’s local position.
            pos = self.mapFromScene(event.scenePos())

            # Calculate the minimum width and height based on the class name text length
            longest_string_width = max(self.class_name_text.boundingRect().width(), 0) + self.default_margin * 2
            min_string_height = (self.class_name_text.boundingRect().height()) + self.default_margin * 2

            # Update the size of the box based on the specific handle being dragged
            if self.current_handle == 'top_left':
                new_rect.setTopLeft(pos)  # Adjust the top-left corner based on the new mouse position
            elif self.current_handle == 'top_right':
                new_rect.setTopRight(pos)  # Adjust the top-right corner based on the new mouse position
            elif self.current_handle == 'bottom_left':
                new_rect.setBottomLeft(pos)  # Adjust the bottom-left corner based on the new mouse position
            elif self.current_handle == 'bottom_right':
                new_rect.setBottomRight(pos)  # Adjust the bottom-right corner based on the new mouse position

            # Calculate the new width and height of the box based on the mouse movement
            new_width = new_rect.width()
            new_height = new_rect.height()

            # Ensure the box does not shrink smaller than the minimum width based on text
            if new_width >= longest_string_width:
                new_rect.setWidth(new_width)
            else:
                new_rect.setWidth(longest_string_width)  # Apply minimum width

            # Ensure the box does not shrink smaller than the minimum height based on text
            if new_height >= min_string_height:
                new_rect.setHeight(new_height)
            else:
                new_rect.setHeight(min_string_height)  # Apply minimum height

            # Apply the new rectangle dimensions to the UML box
            self.setRect(new_rect)

            # Update the internal contents of the box (e.g., class name position)
            self.update_box()
        else:
            super().mouseMoveEvent(event)  # Call the parent method if not resizing
        
    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to stop dragging or resizing.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        if self.is_box_dragged:
            event.accept()
            self.is_box_dragged = False  # Reset dragging flag
        elif self.is_resizing:
            self.is_resizing = False  # Reset resizing flag
            self.current_handle = None  # Reset current handle

        super().mouseReleaseEvent(event)

    #################################################################

###################################################################################################

def main():
    app = QtWidgets.QApplication(sys.argv)

    # Create a scene and a view
    scene = QtWidgets.QGraphicsScene()
    view = QtWidgets.QGraphicsView(scene)

    # Create an instance of UMLTestBox
    interface = None  # Replace with actual interface object if needed
    uml_box = UMLTestBox(interface)
    scene.addItem(uml_box)

    # Show the view
    view.setGeometry(100, 100, 1000, 1000)
    view.show()

    sys.exit(app.exec_())

###################################################################################################

if __name__ == "__main__":
    main()