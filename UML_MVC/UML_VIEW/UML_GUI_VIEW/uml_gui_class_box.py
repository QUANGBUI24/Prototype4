import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from functools import partial
from typing import Dict, List

###################################################################################################
# ADD ROOT PATH #
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.append(root_path)

from UML_ENUM_CLASS.uml_enum import BoxDefaultStat as Default
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_editable_text_item import UMLEditableTextItem as Text

###################################################################################################

class UMLClassBox(QtWidgets.QGraphicsRectItem):
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
        self.field_list: Dict = field_list if field_list is not None else {}
        self.field_name_list: List = []
        
        self.method_list: Dict = method_list if method_list is not None else {}
        self.method_name_list: Dict = {}
        
        self.parameter_list: Dict = parameter_list if parameter_list is not None else {}
        self.parameter_name_list: List = []
        
        self.handles_list: List = []
        self.connection_points_list: List = []

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
        self.is_selected = False
        self.current_handle = None

        #################################
        
        # Define bounding rectangle of the class box
        self.setRect(self.default_box_x, self.default_box_y, self.default_box_width, self.default_box_height)
        # Set border color (Dodger Blue)
        self.setPen(QtGui.QPen(QtGui.QColor(30,144,255)))  
        # Set background color (cyan)
        self.setBrush(QtGui.QBrush(QtGui.QColor(0,255,255)))  
        # Set class box selectable
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        # Set class box movable
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True) 
        # Enable the box to send geometry change events.
        # This allows the box to notify the parent item (the class box) when it moves or is resized.
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        # Enable hover events
        self.setAcceptHoverEvents(True)
        # Class name text box and make it appear at the center of the box.
        self.class_name_text = self.create_text_item(class_name, selectable=True)
        # Connect the text change callback to ensure it re-centers when the text changes.
        self.class_name_text.document().contentsChanged.connect(self.centering_class_name)
        # Create separator below class name
        self.create_separator()
        # Draw first separator
        self.separator_line1.setPen(QtGui.QPen(QtCore.Qt.black))
        # Centering class name initially.
        self.centering_class_name()
        # Create handles for resizing the class box.
        self.create_resize_handles()
        # Create connection point for arrow line.
        self.create_connection_points()

    #################################################################
    ### MEMBER FUNCTIONS ###
    
    #################################
    ## UPDATE BOX AND IS COMPONENTS ##
    
    def update_box(self):
        """
        Update the dimensions and layout of the UML box.

        This method recalculates and updates all aspects of the UML box, including:
        - Repositioning the class name.
        - Adjusting the box height and width.
        - Updating the positions of resize handles.
        - Adjusting connection points for relationships.
        - Aligning fields, methods, and parameters.
        - Updating the separators between different sections (class name, fields, methods).

        This ensures that all elements in the UML box are correctly positioned and scaled 
        based on the current content of the box.
        """
        # Reposition the class name in the center of the UML box
        self.centering_class_name()

        # Adjust the box's height and width based on its contents
        self.update_box_dimension()

        # Update the position of the resize handles at the corners of the UML box
        self.update_handle_positions()

        # Update the connection points (e.g., for relationships) around the box
        self.update_connection_point_positions()

        # Align the fields within the UML box
        self.update_field_alignment()

        # Align the methods and parameters within the UML box
        self.update_method_and_param_alignment()

        # Update the separators between the class name, fields, and methods
        self.update_separators()

    def update_box_dimension(self):
        """
        Recalculate and update the dimensions of the UML box.

        This function calculates the total height of the UML box based on the height of the class name,
        fields, methods, and parameters. The width is set to the larger of the default width or the maximum width 
        required by the text contents (fields, methods, or parameters). If the box is not being manually resized 
        or dragged, it adjusts the box dimensions to fit the content.

        Steps:
        1. Get the height of the class name, fields, methods, and parameters.
        2. Calculate the total height and maximum width required.
        3. Update the box size if it is not currently being resized or dragged.
        """
        # Get the height of the class name text
        class_name_height = self.class_name_text.boundingRect().height()

        # Get the total height of the fields section
        fields_text_height = self.get_field_text_height()

        # Get the total height of the methods section
        method_text_height = self.get_method_text_height()

        # Get the total height of the parameters section
        parameter_text_height = self.get_total_param_text_height()

        # Calculate the total height required for the box, including margins
        total_height = (class_name_height + fields_text_height + method_text_height 
                        + parameter_text_height + self.default_margin * 2)

        # Calculate the maximum width required by the content
        max_width = max(self.default_box_width, self.get_maximum_width()) + self.default_margin * 2
        print(f"Max Width = {max_width}")  # Debugging print statement to show the calculated width

        # If the box is not being resized manually or dragged, adjust the size of the box
        # Ensure the total height is greater than the current height before resizing
        if not self.is_resizing and not self.is_box_dragged and total_height >= self.rect().height():
            # Update the rectangle (box) size with the new width and height
            self.setRect(0, 0, max_width, total_height)
        
    def update_separators(self):
        """
        Update positions of the separator lines based on current box size.
        This function keeps the separator anchored at a fixed y-position relative to the class name.
        """
        if hasattr(self, 'separator_line1'):
            # Update the separator line based on the current size of the UML box
            class_name_height = self.class_name_text.boundingRect().height()
            y_pos = self.rect().topLeft().y() + class_name_height + self.default_margin
            # Set the new position of the separator line
            self.separator_line1.setLine(
                self.rect().topLeft().x(), y_pos, 
                self.rect().topRight().x(), y_pos
            )
        if hasattr(self, 'separator_line2') and self.separator_line2.scene() == self.scene():
            if len(self.method_name_list) > 0:
                class_name_height = self.class_name_text.boundingRect().height()
                field_section_height = self.get_field_text_height()
                y_pos = self.rect().topLeft().y() + class_name_height + field_section_height + self.default_margin
                self.separator_line2.setLine(
                self.rect().topLeft().x(), y_pos, 
                self.rect().topRight().x(), y_pos
                )
            else:
                self.scene().removeItem(self.separator_line2)
                
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
        
    def update_field_alignment(self):
        """
        Align field text items in the UML class box row by row.

        Each field will be displayed on a new line, aligned to the left of the box.
        """
        # Starting y-position for the first field (below the class name)
        y_offset = self.class_name_text.boundingRect().height() + self.default_margin

        for field_name in self.field_name_list:
            # Get the text item for the field
            field_text = self.field_list[field_name]
        
            # Calculate the x-position to center the field text horizontally
            field_x_pos = self.rect().topLeft().x() + self.default_margin
        
            # Set the position of the field text, each field below the previous one
            field_text.setPos(field_x_pos, self.rect().topLeft().y() + y_offset)
        
            # Increment y_offset for the next field (adding field height and margin)
            y_offset += field_text.boundingRect().height()
            
    def update_method_and_param_alignment(self):
        """
        Align methods and parameters in the UML class box row by row.

        Each method will be displayed on a new line, with its parameters indented beneath it.
        """
        # Starting y-position for the first method (below the class name and fields)
        y_offset = self.class_name_text.boundingRect().height() + self.get_field_text_height() + self.default_margin

        # Iterate through each method and align them, along with their parameters
        for method_name in self.method_name_list:
            # Get the method text item
            method_text = self.method_list[method_name]

            # Calculate the x-position for the method text (aligned to the left)
            method_x_pos = self.rect().topLeft().x() + self.default_margin

            # Set the position of the method text item
            method_text.setPos(method_x_pos, self.rect().topLeft().y() + y_offset)

            # Update y_offset for the next method or parameter (incremented by the height of this method)
            y_offset += method_text.boundingRect().height()

            # Align parameters under the current method
            if method_name in self.method_name_list:
                for param_name in self.method_name_list[method_name]:
                    # Get the parameter text item
                    param_text = self.parameter_list[param_name]

                    # Calculate the x-position for the parameter text (indented)
                    param_x_pos = self.rect().topLeft().x() + self.default_margin * 2

                    # Set the position of the parameter text item
                    param_text.setPos(param_x_pos, self.rect().topLeft().y() + y_offset)

                    # Update y_offset after positioning the parameter (incremented by the height of the parameter)
                    y_offset += param_text.boundingRect().height()
            
    #################################
    
    def create_separator(self, is_first=True):
        """
        Create a separator line between different sections of the UML class box.

        This method is used to visually separate the class name, fields, and methods in the UML class box.
        It creates a horizontal line that spans the width of the UML box and adjusts its position based on 
        the content (class name and fields).

        Args:
            is_first (bool): 
                - If True, creates the first separator line below the class name.
                - If False, creates the second separator line below the fields.

        Steps:
        1. Determine the height of the class name using boundingRect().
        2. For the first separator, place it below the class name with some margin.
        3. For the second separator, place it below the fields section.
        4. Use QGraphicsLineItem to draw the line across the box width.
        """
        
        # Check if it's the first separator (placed below the class name)
        if is_first:
            # Calculate the height of the class name text item to determine where the separator should be positioned.
            class_name_height = self.class_name_text.boundingRect().height()

            # Set the y-position for the separator line just below the class name, leaving a small margin.
            y_pos = self.rect().topLeft().y() + class_name_height + self.default_margin

            # Create the first separator as a horizontal line (QGraphicsLineItem) spanning the entire width of the UML box.
            self.separator_line1 = QtWidgets.QGraphicsLineItem(
                self.rect().topLeft().x(),  # Starting x-coordinate (left side of the box)
                y_pos,                      # Y-coordinate (below the class name)
                self.rect().topRight().x(),  # Ending x-coordinate (right side of the box)
                y_pos,                      # Keep the same y-coordinate to make the line horizontal
                self  # Set the UML class box as the parent for this line item.
            )

        # If it's not the first separator, create the second separator (placed below the fields section)
        else:
            # Calculate the height of the class name to start the separator calculation.
            class_name_height = self.class_name_text.boundingRect().height()

            # Calculate the total height of all the field text items to place the separator correctly.
            field_section_height = self.get_field_text_height()

            # Set the y-position for the second separator line just below the fields, with some margin.
            y_pos = self.rect().topLeft().y() + class_name_height + field_section_height + self.default_margin

            # Create the second separator as a horizontal line (QGraphicsLineItem) spanning the entire width of the UML box.
            self.separator_line2 = QtWidgets.QGraphicsLineItem(
                self.rect().topLeft().x(),  # Starting x-coordinate (left side of the box)
                y_pos,                      # Y-coordinate (below the fields section)
                self.rect().topRight().x(),  # Ending x-coordinate (right side of the box)
                y_pos,                      # Keep the same y-coordinate to make the line horizontal
                self  # Set the UML class box as the parent for this line item.
            )
           
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
            handle.setPen(QtGui.QPen(QtGui.QColor(30,144,255)))  # Dodger Blue border
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

    #################################
    ## CLASS NAME TEXT RELATED ##
    
    def create_text_item(self, text:str, selectable=False, is_field=None, is_method=None, is_parameter=None):
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
        if selectable:
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
        self.class_name_text.setPos(class_name_x_pos, self.rect().topLeft().y() + self.default_margin / 2)

    #################################
    ### UML CLASS OPERATIONS ###
    
    ## CLASS OPERATION ##
    def rename_class(self):
        """
        Rename the class displayed in the UML box.

        This method prompts the user to input a new name for the class. 
        If the user confirms and enters a valid name, the class name is updated 
        and the box is refreshed to reflect the new name.
        """
        # Display a dialog asking the user for the new class name
        class_name, ok = QtWidgets.QInputDialog.getText(None, "Rename Class", f"Enter new name for class '{self.class_name_text.toPlainText()}'")
        
        # If the user confirms and provides a valid name, update the class name
        if ok and class_name:
            self.class_name_text.setPlainText(class_name)  # Set the new name in the UML box
            self.update_box()  # Update the box layout to reflect the change

    ## FIELD OPERATION ##
    def add_field(self):
        """
        Add a new field to the UML class.

        This method prompts the user to input a new field name. 
        If confirmed, the field is added to the class, and the box layout is updated.
        """
        # Display a dialog asking the user for the new field name
        field_name, ok = QtWidgets.QInputDialog.getText(None, "Add Field", "Enter field name:")

        # If the user confirms and provides a valid name, create and add the field
        if ok and field_name:
            # Create a text item for the field and add it to the list
            field_text = self.create_text_item(field_name, is_field=True, selectable=True)
            self.field_list[field_name] = field_text  # Add the field to the internal list
            self.field_name_list.append(field_name)  # Track the field name in the name list
            self.update_box()  # Update the box to reflect the changes

    def delete_field(self):
        """
        Remove an existing field from the UML class.

        This method allows the user to select a field from a list of existing fields to remove. 
        The field is removed from the class, and the UML box is updated.
        """
        if self.field_name_list:
            # Display a dialog asking the user to select a field to remove
            field_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Field", "Select field to remove:", self.field_name_list, 0, False)

            # If the user confirms, remove the selected field from the class
            if ok and field_name:
                self.field_name_list.remove(field_name)  # Remove from the name list
                self.scene().removeItem(self.field_list.pop(field_name))  # Remove the text item from the scene
                self.update_box()  # Update the box to reflect the changes
        else:
            # Show a warning if there are no fields to remove
            QtWidgets.QMessageBox.warning(None, "Warning", "No fields to remove.")

    def rename_field(self):
        """
        Rename an existing field in the UML class.

        The user selects a field to rename, then provides a new name for that field.
        The field name is updated, and the UML box is refreshed.
        """
        if self.field_name_list:
            # Display a dialog to choose the field to rename
            field_name, ok = QtWidgets.QInputDialog.getItem(None, "Change Field Name", "Select field to change:", self.field_name_list, 0, False)

            if ok and field_name:
                # Ask for the new name for the selected field
                new_name, ok = QtWidgets.QInputDialog.getText(None, "Rename Field", f"Enter new name for the field '{field_name}':")
                
                if ok and new_name:
                    # Update the field name in the list and refresh the display
                    if field_name in self.field_list:
                        self.field_list[new_name] = self.field_list.pop(field_name)  # Rename the field in the internal list
                        self.field_list[new_name].setPlainText(new_name)  # Set the new field name
                        self.field_name_list[self.field_name_list.index(field_name)] = new_name  # Update the name list
                        self.update_box()  # Refresh the box display
        else:
            # Show a warning if there are no fields to rename
            QtWidgets.QMessageBox.warning(None, "Warning", "No fields to change.")

    ## METHOD OPERATIONS ##
    def add_method(self):
        """
        Add a new method to the UML class.

        The user is prompted to input the method name. The method is then added to the class,
        and the UML box is updated.
        """
        # Display a dialog asking for the new method name
        method_name, ok = QtWidgets.QInputDialog.getText(None, "Add Method", "Enter method name:")

        # If the user confirms and provides a valid method name, add it to the UML box
        if ok and method_name:
            method_text = self.create_text_item(method_name + "()", is_method=True, selectable=True)
            self.method_list[method_name] = method_text  # Store the method text
            self.method_name_list[method_name] = []  # Track the method's parameters
            if len(self.method_name_list) == 1:  # If this is the first method, create a separator
                self.create_separator(is_first=False)
            self.update_box()  # Update the UML box

    def delete_method(self):
        """
        Remove an existing method from the UML class.

        The user selects a method to remove from a list. If confirmed, the method and its parameters 
        are deleted from the class, and the UML box is updated.
        """
        if self.method_list:
            # Ask the user to select a method to remove
            method_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Method", "Select method to remove:", self.method_name_list, 0, False)

            if ok and method_name:
                # Remove associated parameters and the method itself
                for param_name in self.method_name_list[method_name]:
                    self.scene().removeItem(self.parameter_list.pop(param_name))  # Remove parameter
                self.method_name_list.pop(method_name)  # Remove from method list
                self.scene().removeItem(self.method_list.pop(method_name))  # Remove the method text
                self.update_box()  # Refresh the UML box
        else:
            # Show a warning if there are no methods to remove
            QtWidgets.QMessageBox.warning(None, "Warning", "No method to remove.")

    def rename_method(self):
        """
        Rename an existing method in the UML class.

        The user selects a method to rename and provides a new name. The method name is updated,
        and the UML box is refreshed.
        """
        if self.method_name_list:
            # Prompt the user to select the method to rename
            method_name, ok = QtWidgets.QInputDialog.getItem(None, "Change Method Name", "Select method to change:", self.method_name_list, 0, False)

            if ok and method_name:
                # Prompt for the new name
                new_name, ok = QtWidgets.QInputDialog.getText(None, "Rename Method", f"Enter new name for the method '{method_name}':")
                
                if ok and new_name:
                    # Update the method name and refresh the UI
                    if method_name in self.method_list:
                        self.method_list[new_name] = self.method_list.pop(method_name)  # Update the method name in the list
                        self.method_list[new_name].setPlainText(new_name + "()")  # Set the new name in the UML box
                        self.method_name_list[new_name] = self.method_name_list.pop(method_name)  # Track the change
                        self.update_box()  # Refresh the UML box display
        else:
            # Show a warning if there are no methods to rename
            QtWidgets.QMessageBox.warning(None, "Warning", "No methods to change.")

    ## PARAMETER OPERATIONS ##
    def add_param(self):
        """
        Add a new parameter to a method in the UML class.

        The user selects a method and provides a parameter name, which is then added to the method.
        The UML box is updated to reflect the new parameter.
        """
        if self.method_name_list:
            # Ask the user to choose a method to add a parameter to
            method_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Method Name", "Select method to add parameter:", list(self.method_name_list.keys()), 0, False)

            if ok and method_name:
                # Ask for the parameter name
                param_name, ok = QtWidgets.QInputDialog.getText(None, "Add Parameter", "Enter parameter name:")

                if ok and param_name:
                    # Add the parameter to the selected method and update the UML box
                    param_text = self.create_text_item(param_name , is_parameter=True, selectable=True)
                    self.method_name_list[method_name].append(param_name)  # Track the parameter
                    self.parameter_list[param_name] = param_text  # Store the parameter text
                    self.parameter_name_list.append(param_name)  # Add to the list of parameter names
                    self.update_box()  # Update the UML box
        else:
            # Show a warning if there are no methods available
            QtWidgets.QMessageBox.warning(None, "Warning", "No methods to choose.")

    def delete_param(self):
        """
        Remove a parameter from a method in the UML class.

        The user selects a method and parameter to remove, and if confirmed, the parameter is deleted 
        from the method. The UML box is updated.
        """
        if self.method_name_list:
            # Ask the user to choose a method to remove a parameter from
            method_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Method Name", "Select method to remove parameter:", list(self.method_name_list.keys()), 0, False)

            if ok and method_name:
                # Check if the selected method has parameters
                if self.method_name_list[method_name]:
                    # Ask the user to choose the parameter to remove
                    param_name, ok = QtWidgets.QInputDialog.getItem(None, "Delete Parameter", "Choose parameter name to remove:", self.method_name_list[method_name], 0, False)

                    if ok and param_name:
                        # Remove the parameter and update the UML box
                        self.scene().removeItem(self.parameter_list.pop(param_name))  # Remove from the scene
                        self.method_name_list[method_name].remove(param_name)  # Remove from method's parameter list
                        self.parameter_name_list.remove(param_name)  # Remove from the global parameter list
                        self.update_box()  # Refresh the UML box
                else:
                    # Show a warning if there are no parameters to remove
                    QtWidgets.QMessageBox.warning(None, "Warning", "No parameters to choose.")
        else:
            # Show a warning if there are no methods available
            QtWidgets.QMessageBox.warning(None, "Warning", "No methods to choose.")

    def rename_param(self):
        """
        Rename a parameter in the UML class.

        The user selects a method and a parameter to rename, then provides a new name for the parameter.
        The parameter name is updated, and the UML box is refreshed.
        """
        if self.method_name_list:
            # Ask the user to choose a method containing the parameter
            method_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Method Name", "Select method:", list(self.method_name_list.keys()), 0, False)

            if ok and method_name:
                # Check if the selected method has parameters
                if self.method_name_list[method_name]:
                    # Ask the user to choose the parameter to rename
                    param_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Parameter", "Choose parameter name to rename:", self.method_name_list[method_name], 0, False)

                    if ok and param_name:
                        # Ask for the new parameter name
                        new_name, ok = QtWidgets.QInputDialog.getText(None, "Rename Parameter", "Enter new parameter name:")

                        if ok and new_name:
                            # Update the parameter name and refresh the UML box
                            param_list = self.method_name_list[method_name]
                            param_list[param_list.index(param_name)] = new_name  # Update in the method's parameter list
                            self.parameter_list[new_name] = self.parameter_list.pop(param_name)  # Update the parameter list
                            self.parameter_list[new_name].setPlainText(new_name)  # Set the new name in the UI
                            self.parameter_name_list[self.parameter_name_list.index(param_name)] = new_name  # Track the change
                            self.update_box()  # Refresh the UML box
                else:
                    # Show a warning if there are no parameters to rename
                    QtWidgets.QMessageBox.warning(None, "Warning", "No parameters to choose.")
        else:
            # Show a warning if there are no methods available
            QtWidgets.QMessageBox.warning(None, "Warning", "No methods to choose.")
            
    def replace_parameter(self):
        """
        Replace parameters for a method in the UML class.

        This function allows the user to input multiple parameter names, which are 
        then added as individual parameters for the selected method. It will replace 
        all existing parameters for that method with the new ones.

        Steps:
        1. User selects a method from a list of existing methods.
        2. User enters multiple parameters as a string, separated by commas.
        3. Each parameter is created as a text item and added to the method.
        4. Existing parameters are replaced by the new ones.
        """
        # Ensure there are methods to choose from
        if self.method_name_list:
            # Select the method to replace parameters for
            method_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Method Name", 
                                                             "Select method to replace parameters:", 
                                                             list(self.method_name_list.keys()), 0, False)
            if ok and method_name:
                # Prompt user to enter the new parameters as a comma-separated string
                param_string, ok = QtWidgets.QInputDialog.getText(None, "Replace Parameters", 
                                                                  "Enter new parameters (comma-separated):")
                if ok and param_string:
                    # Split the input string by commas to form a list of parameters
                    new_param_list = [param.strip() for param in param_string.split(",") if param.strip()]

                    # Clear current parameters
                    for param_name in self.method_name_list[method_name]:
                        self.scene().removeItem(self.parameter_list.pop(param_name))
                    
                    # Clear the method's parameter list
                    self.method_name_list[method_name].clear()
                    
                    # Add new parameters to the method
                    for new_param in new_param_list:
                        param_text = self.create_text_item(new_param, is_parameter=True, selectable=True)
                        self.method_name_list[method_name].append(new_param)
                        self.parameter_list[new_param] = param_text
                        self.parameter_name_list.append(new_param)
                    
                    # Update the box to reflect changes
                    self.update_box()
        else:
            # Display a warning if no methods are available
            QtWidgets.QMessageBox.warning(None, "Warning", "No methods available to replace parameters.")
                        
    #################################
    ## MOUSE EVENT RELATED ##
    
    def contextMenuEvent(self, event):
        """Show context menu when right-clicking on the UMLClassBox"""
        #################################
        # Create the context menu
        contextMenu = QtWidgets.QMenu()
        
        # Class option
        rename_class_button = contextMenu.addAction("Rename Class")
        
        # Add a separator before the field options
        contextMenu.addSeparator()
        
        # Add field options
        add_field_button = contextMenu.addAction("Add Field")
        delete_field_button = contextMenu.addAction("Delete Field")
        rename_field_button = contextMenu.addAction("Rename Field")
        
        # Add a separator before the method options
        contextMenu.addSeparator()
        
        # Add method options
        add_method_button = contextMenu.addAction("Add Method")
        delete_method_button = contextMenu.addAction("Delete Method")
        rename_method_button = contextMenu.addAction("Rename Method")
        
        # Add a separator before the parameter options
        contextMenu.addSeparator()
        
        # Add parameter options
        add_parameter_button = contextMenu.addAction("Add Parameter")
        delete_parameter_button = contextMenu.addAction("Delete Parameter")
        rename_parameter_button = contextMenu.addAction("Rename Parameter")
        replace_parameter_button = contextMenu.addAction("Replace Parameter")

        #################################
        # Connect class option to method
        rename_class_button.triggered.connect(self.rename_class)
        
        # Connect field options to fields
        add_field_button.triggered.connect(self.add_field)
        delete_field_button.triggered.connect(self.delete_field)
        rename_field_button.triggered.connect(self.rename_field)
        
        # Connect method options to methods
        add_method_button.triggered.connect(self.add_method)
        delete_method_button.triggered.connect(self.delete_method)
        rename_method_button.triggered.connect(self.rename_method)
        
        # Connect parameter options to parameters
        add_parameter_button.triggered.connect(self.add_param)
        delete_parameter_button.triggered.connect(self.delete_param)
        rename_parameter_button.triggered.connect(self.rename_param)
        replace_parameter_button.triggered.connect(self.replace_parameter)

        # Execute the context menu and get the selected action
        contextMenu.exec_(event.screenPos())
        self.update_box()

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
                        self.update_box()
                        return
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """
        Handle the mouse movement event for resizing the UML box.

        This function updates the size of the UML box based on the handle being dragged during resizing.
        It ensures that the box maintains a minimum width and height based on the content (class name, fields, methods, etc.)
        to prevent them from being cut off. The handle being dragged determines which part of the box 
        (top-left, top-right, bottom-left, or bottom-right) is adjusted. The new dimensions are calculated 
        based on the mouse position, and the box is updated accordingly.

        Parameters:
            event (QGraphicsSceneMouseEvent): The event that provides the mouse movement data.
        """
        # Check if the box is being resized and if a specific handle is active
        if self.is_resizing and self.current_handle:
            new_rect = self.rect()  # Get the current rectangle (box) dimensions
            
            # Convert the global mouse position to the local coordinate system of the box.
            pos = self.mapFromScene(event.scenePos())

            # Calculate the total height of all elements (class name, fields, methods, parameters)
            class_name_height = self.class_name_text.boundingRect().height()
            fields_text_height = self.get_field_text_height()
            method_text_height = self.get_method_text_height()
            param_text_height = self.get_total_param_text_height()
            total_height = class_name_height + fields_text_height + method_text_height + param_text_height + self.default_margin * 2
            
            # Set the maximum width and minimum height for resizing
            max_width = max(self.default_box_width, self.get_maximum_width()) + self.default_margin * 2
            min_string_height = total_height

            # Adjust size based on the specific handle being dragged
            if self.current_handle == 'top_left':
                # Resize from the top-left corner
                new_width = self.rect().right() - pos.x()  # Calculate the new width
                new_height = self.rect().bottom() - pos.y()  # Calculate the new height

                # If width and height are valid, resize the box and adjust the position of the left and top sides
                if new_width > max_width:
                    new_rect.setWidth(new_width)
                    new_rect.moveLeft(pos.x())  # Move the left side
                if new_height > min_string_height:
                    new_rect.setHeight(new_height)
                    new_rect.moveTop(pos.y())  # Move the top side

            elif self.current_handle == 'top_right':
                # Resize from the top-right corner
                new_width = pos.x() - self.rect().left()
                new_height = self.rect().bottom() - pos.y()

                if new_width > max_width:
                    new_rect.setWidth(new_width)
                if new_height > min_string_height:
                    new_rect.setHeight(new_height)
                    new_rect.moveTop(pos.y())  # Move the top side

            elif self.current_handle == 'bottom_left':
                # Resize from the bottom-left corner
                new_width = self.rect().right() - pos.x()
                new_height = pos.y() - self.rect().top()

                if new_width > max_width:
                    new_rect.setWidth(new_width)
                    new_rect.moveLeft(pos.x())  # Move the left side
                if new_height > min_string_height:
                    new_rect.setHeight(new_height)

            elif self.current_handle == 'bottom_right':
                # Resize from the bottom-right corner
                new_width = pos.x() - self.rect().left()
                new_height = pos.y() - self.rect().top()

                if new_width > max_width:
                    new_rect.setWidth(new_width)
                if new_height > min_string_height:
                    new_rect.setHeight(new_height)

            # Apply the new rectangle dimensions to the UML box
            self.setRect(new_rect)
            
            # Update the internal layout and content of the box (e.g., text, handles, connection points)
            self.update_box()
        else:
            super().mouseMoveEvent(event)  # Call the parent method if not resizing

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to stop dragging or resizing the UML box.
        
        This method stops the resizing or dragging action once the mouse is released, 
        and it may snap the box to the nearest grid position if the box is being dragged.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        # If the box was being dragged, snap it to the nearest grid and stop dragging
        if self.is_box_dragged:
            self.snap_to_grid()  # Snap the box to the nearest grid position
            event.accept()
            self.is_box_dragged = False  # Reset dragging flag

        # If the box was being resized, stop the resizing process
        elif self.is_resizing:
            self.is_resizing = False  # Reset resizing flag
            self.current_handle = None  # Reset the handle being resized
        super().mouseReleaseEvent(event)  # Call the parent method

    #################################################################
    ### UTILITY FUNCTIONS ###
    
    def snap_to_grid(self, current_grid_size=20):
        """
        Snap the UML box to the nearest grid position.

        This method calculates the nearest grid coordinates based on the current position of the box
        and adjusts the position to align it with the grid. The grid size can be adjusted using the parameter.

        Parameters:
        - current_grid_size (int): The size of the grid to snap to (default is 20).
        """
        grid_size = current_grid_size * self.transform().m11()  # Adjust for zoom factor
        pos = self.pos()  # Get the current position of the box

        # Calculate new x and y positions by snapping to the nearest grid points
        new_x = round(pos.x() / grid_size) * grid_size
        new_y = round(pos.y() / grid_size) * grid_size

        # Update the box's position and internal content
        self.setPos(new_x, new_y)
        self.update_box()

    def get_field_text_height(self):
        """
        Calculate the total height of all field text items in the box.
        
        Returns:
        - field_tex_height (int): The total height of all field text items.
        """
        field_tex_height = 0
        # Sum the heights of all field text items
        for field_name in self.field_name_list:
            field_text = self.field_list[field_name]  # Get the text item for each field
            field_tex_height += field_text.boundingRect().height()
        return field_tex_height

    def get_method_text_height(self):
        """
        Calculate the total height of all method text items in the box.
        
        Returns:
        - method_tex_height (int): The total height of all method text items.
        """
        method_tex_height = 0
        # Sum the heights of all method text items
        for method_name in self.method_name_list:
            method_text = self.method_list[method_name]  # Get the text item for each method
            method_tex_height += method_text.boundingRect().height()
        return method_tex_height

    def get_param_text_height_of_single_method(self, method_name):
        """
        Calculate the total height of all parameter text items for a specific method.
        
        Parameters:
        - method_name (str): The name of the method to get the parameter heights for.
        
        Returns:
        - param_tex_height (int): The total height of all parameter text items for the method.
        """
        param_tex_height = 0
        # Sum the heights of all parameter text items for the specified method
        for param_name in self.method_name_list[method_name]:
            param_text = self.parameter_list[param_name]  # Get the text item for each parameter
            param_tex_height += param_text.boundingRect().height()
        return param_tex_height

    def get_total_param_text_height(self):
        """
        Calculate the total height of all parameter text items for all methods in the box.
        
        Returns:
        - total_param_tex_height (int): The total height of all parameter text items.
        """
        total_param_tex_height = 0
        # Loop through all methods and sum the heights of their parameter text items
        for method_name in self.method_name_list:
            total_param_tex_height += self.get_param_text_height_of_single_method(method_name)
        return total_param_tex_height

    def get_maximum_width(self):
        """
        Calculate the maximum width of the UML box based on the widths of its fields, methods, and parameters.

        This function ensures that the box has enough width to display all content without truncation.

        Returns:
        - max_width (int): The maximum width required for the box based on its contents.
        """
        # Get the maximum width of all field text items
        max_field_width = max([self.field_list[field_name].boundingRect().width() for field_name in self.field_name_list], default=0)
        
        # Get the maximum width of all method text items
        max_method_width = max([self.method_list[method_name].boundingRect().width() for method_name in self.method_name_list], default=0)
        
        # Get the maximum width of all parameter text items
        max_param_width = 0
        for method_name in self.method_name_list:
            # Check for parameters under the current method and calculate their widths
            if method_name in self.method_name_list:
                param_widths = [self.parameter_list[param_name].boundingRect().width() for param_name in self.method_name_list[method_name]]
                max_param_width = max(max_param_width, max(param_widths, default=0))
        
        # Return the largest width between fields, methods, and parameters
        return max(max_field_width, max_method_width, max_param_width)

###################################################################################################