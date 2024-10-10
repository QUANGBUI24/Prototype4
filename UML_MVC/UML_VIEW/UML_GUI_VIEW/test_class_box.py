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
        self.connection_point_size = 8
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
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))  
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
        # Calculate heights of all text sections
        class_name_height = self.class_name_text.boundingRect().height()
        
        # Set positions of text items relative to each other #
        self.centering_class_name()
        
    def create_resize_handles(self):
        """
        Create resize handles at 4 corners of the class box.
        """
       # Create the 4 corner handles
        top_left_handle = QtWidgets.QGraphicsEllipseItem(self)
        top_left_handle.setRect(self.rect().x() - self.handle_size / 2, self.rect().y() - self.handle_size / 2, self.handle_size, self.handle_size)

        top_right_handle = QtWidgets.QGraphicsEllipseItem(self)
        top_right_handle.setRect(self.rect().right() - self.handle_size / 2, self.rect().y() - self.handle_size / 2, self.handle_size, self.handle_size)

        bottom_left_handle = QtWidgets.QGraphicsEllipseItem(self)
        bottom_left_handle.setRect(self.rect().x() - self.handle_size / 2, self.rect().bottom() - self.handle_size / 2, self.handle_size, self.handle_size)

        bottom_right_handle = QtWidgets.QGraphicsEllipseItem(self)
        bottom_right_handle.setRect(self.rect().right() - self.handle_size / 2, self.rect().bottom() - self.handle_size / 2, self.handle_size, self.handle_size)

        # Store the handles in a dictionary for easy reference
        self.handles_list = {
            'top_left': top_left_handle,
            'top_right': top_right_handle,
            'bottom_left': bottom_left_handle,
            'bottom_right': bottom_right_handle,
        }

        for handle_name, handle in self.handles_list.items():
            # Set the pen (border color) for the resize handle to black
            handle.setPen(QtGui.QPen(QtGui.QColor(0,0,0))) 

            # Set the brush (fill color) for the resize handle to white
            handle.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))

            # Enable the handle to send geometry change events.
            # This allows the handle to notify the parent item (the class box) when it moves or is resized.
            handle.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
            
            # Enable hover events for the handle.
            # This allows the handle to receive hoverEnter and hoverLeave events,
            # triggering custom actions like changing the cursor when the mouse hovers over the handle.
            handle.setAcceptHoverEvents(True)

            # Override the default hoverEnterEvent with a custom event handler.
            # The `partial` function is used to pass the `handle_name` (e.g., 'top_left', 'bottom_right') to the event handler.
            # This ensures that each handle has its own behavior depending on which one is hovered.
            handle.hoverEnterEvent = partial(self.handle_hoverEnterEvent, handle_name=handle_name)

            # Set the hoverLeaveEvent to a custom handler.
            # When the mouse leaves the handle, this event will reset the cursor to the default state.
            handle.hoverLeaveEvent = self.handle_hoverLeaveEvent
    
    def update_handle_positions(self):
        """Update the handle positions based on the new rectangle."""
        self.handles_list['top_left'].setRect(self.rect().x() - self.handle_size / 2, self.rect().y() - self.handle_size / 2, self.handle_size, self.handle_size)
        self.handles_list['top_right'].setRect(self.rect().right() - self.handle_size / 2, self.rect().y() - self.handle_size / 2, self.handle_size, self.handle_size)
        self.handles_list['bottom_left'].setRect(self.rect().x() - self.handle_size / 2, self.rect().bottom() - self.handle_size / 2, self.handle_size, self.handle_size)
        self.handles_list['bottom_right'].setRect(self.rect().right() - self.handle_size / 2, self.rect().bottom() - self.handle_size / 2, self.handle_size, self.handle_size)
    
    def create_connection_points(self):
        """
        Create resize handles at 4 corners of the class box.
        """
       # Define the positions for each connection point
        top_x = self.rect().width() / 2 - 4
        top_y = self.pos().y() - 5
        
        bot_x = self.rect().width() / 2 - 4
        bot_y = self.pos().y() + self.rect().height() - 5
        
        left_x = self.pos().x() - 5
        left_y = self.rect().height() / 2
        
        right_x = self.rect().width() - 5
        right_y = self.rect().height() / 2

        self.handles_list = {
        'top': QtWidgets.QGraphicsEllipseItem(top_x, top_y, self.connection_point_size, self.connection_point_size, self),
        'bottom': QtWidgets.QGraphicsEllipseItem(bot_x, bot_y, self.connection_point_size, self.connection_point_size, self),
        'left': QtWidgets.QGraphicsEllipseItem(left_x, left_y, self.connection_point_size, self.connection_point_size, self),
        'right': QtWidgets.QGraphicsEllipseItem(right_x, right_y, self.connection_point_size, self.connection_point_size, self),
        }
        
        for connection_point_name, point in self.handles_list.items():
            # Set the pen (border color) for the resize handle to black
            point.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0))) 

            # Set the brush (fill color) for the resize handle to white
            point.setBrush(QtGui.QBrush(QtGui.QColor(50,205,50)))

            # Make the point not movable
            point.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            
            # Make the point not selectable
            point.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)

            # Enable hover events for the handle.
            # This allows the handle to receive hoverEnter and hoverLeave events,
            # triggering custom actions like changing the cursor when the mouse hovers over the handle.
            point.setAcceptHoverEvents(True)

            # Override the default hoverEnterEvent with a custom event handler.
            # The `partial` function is used to pass the `handle_name` (e.g., 'top_left', 'bottom_right') to the event handler.
            # This ensures that each handle has its own behavior depending on which one is hovered.
            point.hoverEnterEvent = partial(self.handle_hoverEnterEvent, handle_name=connection_point_name)

            # Set the hoverLeaveEvent to a custom handler.
            # When the mouse leaves the handle, this event will reset the cursor to the default state.
            point.hoverLeaveEvent = self.handle_hoverLeaveEvent
    
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
        # Get the current width of the UML class box (the rectangle that represents the class).
        box_width = self.rect().width()
    
        # Get the width of the class name text using its bounding rectangle.
        class_name_width = self.class_name_text.boundingRect().width()
    
        # Calculate the x-position to center the class name within the box by subtracting the 
        # text width from the box width and dividing by 2 (horizontal centering).
        class_name_x_pos = (box_width - class_name_width) / 2
    
        # Set the class name's position. The y-position is set to a fixed default margin to 
        # maintain the vertical alignment, while the x-position is the calculated centered value.
        self.class_name_text.setPos(class_name_x_pos, self.default_margin)
    
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
                for handle_name, handle in self.handles.items():
                    if handle.isUnderMouse():
                        self.current_handle = handle_name
                        self.is_resizing = True
                        break
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        # If resizing, update the rectangle size based on the handle being dragged
        if self.is_resizing and self.current_handle:
            rect = self.rect()
            pos = self.mapFromScene(event.scenePos())

            # Update the size of the box based on which handle is being dragged
            if self.current_handle == 'top_left':
                rect.setTopLeft(pos)
            elif self.current_handle == 'top_right':
                rect.setTopRight(pos)
            elif self.current_handle == 'bottom_left':
                rect.setBottomLeft(pos)
            elif self.current_handle == 'bottom_right':
                rect.setBottomRight(pos)
            # Set the new rectangle dimensions
            self.setRect(rect)

            # Ensure that the handles are repositioned
            self.update_handle_positions()
        else:
            super().mouseMoveEvent(event)
        
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
    uml_box = UMLTestBox()
    scene.addItem(uml_box)

    # Show the view
    view.setGeometry(100, 100, 600, 400)
    view.show()

    sys.exit(app.exec_())

###################################################################################################

if __name__ == "__main__":
    main()