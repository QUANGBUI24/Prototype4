###################################################################################################

from PyQt5 import QtWidgets, QtGui, QtCore

###################################################################################################

class MethodItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, method_name, default_margin=None, parent=None):
        super().__init__(QtCore.QRectF(0, 0, 200, 60), parent)
        self.setBrush(QtGui.QColor(255, 255, 200))  # Light yellow color for methods

        # Method Name
        self.method_name_text = QtWidgets.QGraphicsTextItem(method_name, self)
        self.method_name_text.setPos(default_margin, default_margin + 160)

        # Parameters List
        self.parameters = []

        # Parameters Buttons (+ and -)
        self.add_param_button = QtWidgets.QPushButton("+ Parameter")
        self.remove_param_button = QtWidgets.QPushButton("- Parameter")
        self.add_param_button.setStyleSheet("""
    QPushButton {
        background-color: #55ffff;   /* Cyan background */
        color: black;                /* Black text */
        border-radius: 1px;          /* Rounded corners */
        padding: 1px;                /* Padding inside the button */
        border: 1px solid #000000;   /* Black border */
        min-width: 8px;             /* Minimum width */
        min-height: 8px;            /* Minimum height */
        font-size: 10px;             /* Font size */
    }
    QPushButton:hover {
        background-color: #45a049;   /* Darker green when hovered */
    }
""")

        # Style for the remove field button
        self.remove_param_button.setStyleSheet("""
    QPushButton {
        background-color: #55ffff;   /* Cyan background */
        color: black;                /* Black text */
        border-radius: 1px;          /* Rounded corners */
        padding: 1px;                /* Padding inside the button */
        border: 1px solid #000000;   /* Black border */
        min-width: 8px;             /* Minimum width */
        min-height: 8px;            /* Minimum height */
        font-size: 10px;             /* Font size */
    }
    QPushButton:hover {
        background-color: #45a049;   /* Darker green when hovered */
    }
""")
        self.add_param_button_proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.add_param_button_proxy.setWidget(self.add_param_button)
        self.add_param_button_proxy.setPos(10, 30)
        
        self.remove_param_button_proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.remove_param_button_proxy.setWidget(self.remove_param_button)
        self.remove_param_button_proxy.setPos(110, 30)

        # Connect Parameter Buttons
        self.add_param_button.clicked.connect(self.add_parameter)
        self.remove_param_button.clicked.connect(self.remove_parameter)

    def add_parameter(self):
        param_name, ok = QtWidgets.QInputDialog.getText(None, "Add Parameter", "Enter parameter name:")
        if ok and param_name:
            self.parameters.append(param_name)
            

    def remove_parameter(self):
        if self.parameters:
            # Show list of current parameters for the user to choose which one to delete
            param_names = [param.toPlainText() for param in self.parameters]
            param_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Parameter", "Select parameter to remove:", param_names, 0, False)
            if ok and param_name:
                # Find the parameter to remove
                for param in self.parameters:
                    if param.toPlainText() == param_name:
                        self.scene().removeItem(param)
                        self.parameters.remove(param)
                        break
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No parameters to remove.")
            
    def update_param_text(self):
         pass

###################################################################################################

class UMLClassBox(QtWidgets.QGraphicsRectItem):
    """
    A representation of a UML class box with editable sections for class name, fields, and methods.
    Inherits from QGraphicsRectItem to allow graphical representation in a QGraphicsScene.
    """

    #################################################################
    ### CONSTRUCTOR ###

    def __init__(self, interface, class_name="ClassName", field=None, methods=None, parent=None):
        """
        Initializes a new UMLClassBox instance.

        Parameters:
        - class_name (str): The name of the class.
        - field (list): A list of fields (attributes) of the class.
        - methods (list): A list of methods of the class.
        - parent (QGraphicsItem): The parent graphics item.
        """
        super().__init__(parent)
        
        # Interface to communicate with UMLCoreManager
        self.interface = interface  
        
        # Default properties for attributes (fields) and methods if not provided
        self.field: list[str] = field if field is not None else []
        self.methods: list[dict[str, list[str]]] = methods if methods is not None else []

        # Default size and margin settings
        self.default_width = 150
        self.default_margin = 10

        # Define the bounding rectangle size of the class box
        self.setRect(0, 0, self.default_width, 250)
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))  # Set black border
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))  # Set cyan background

        # Create editable text items for the class name, fields, and methods
        self.class_name_text = QtWidgets.QGraphicsTextItem(self)
        self.class_name_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)  # Allow text editing
        self.class_name_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))  # Set text color to black
        self.class_name_text.setPlainText(class_name)  # Set initial class name text
        self.class_name_text.document().contentsChanged.connect(self.update_positions)

        # Create labels for fields and methods
        self.fields_label = QtWidgets.QGraphicsTextItem(self)
        self.fields_label.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.fields_label.setPlainText("Fields")  # Set fields label text
        
        #################################################################
        
        # Create button to add field names, method names, and parameter names
        self.add_field_button = QtWidgets.QPushButton("+")
        self.remove_field_button = QtWidgets.QPushButton("-")
        
        self.add_method_button = QtWidgets.QPushButton("+")
        self.remove_method_button = QtWidgets.QPushButton("-")
        
        # Apply styles to make the buttons rounder and change the colors
        
        # Style for the add field button
        self.add_field_button.setStyleSheet("""
    QPushButton {
        background-color: #55ffff;   /* Cyan background */
        color: black;                /* Black text */
        border-radius: 1px;          /* Rounded corners */
        padding: 1px;                /* Padding inside the button */
        border: 1px solid #000000;   /* Black border */
        min-width: 8px;             /* Minimum width */
        min-height: 8px;            /* Minimum height */
        font-size: 10px;             /* Font size */
    }
    QPushButton:hover {
        background-color: #45a049;   /* Darker green when hovered */
    }
""")

        # Style for the remove field button
        self.remove_field_button.setStyleSheet("""
    QPushButton {
        background-color: #55ffff;   /* Cyan background */
        color: black;                /* Black text */
        border-radius: 1px;          /* Rounded corners */
        padding: 1px;                /* Padding inside the button */
        border: 1px solid #000000;   /* Black border */
        min-width: 8px;             /* Minimum width */
        min-height: 8px;            /* Minimum height */
        font-size: 10px;             /* Font size */
    }
    QPushButton:hover {
        background-color: #45a049;   /* Darker green when hovered */
    }
""")
        self.add_method_button.setStyleSheet("""
    QPushButton {
        background-color: #55ffff;   /* Cyan background */
        color: black;                /* Black text */
        border-radius: 1px;          /* Rounded corners */
        padding: 1px;                /* Padding inside the button */
        border: 1px solid #000000;   /* Black border */
        min-width: 8px;             /* Minimum width */
        min-height: 8px;            /* Minimum height */
        font-size: 10px;             /* Font size */
    }
    QPushButton:hover {
        background-color: #45a049;   /* Darker green when hovered */
    }
""")

        # Style for the remove method button
        self.remove_method_button.setStyleSheet("""
    QPushButton {
        background-color: #55ffff;   /* Cyan background */
        color: black;                /* Black text */
        border-radius: 1px;          /* Rounded corners */
        padding: 1px;                /* Padding inside the button */
        border: 1px solid #000000;   /* Black border */
        min-width: 8px;             /* Minimum width */
        min-height: 8px;            /* Minimum height */
        font-size: 10px;             /* Font size */
    }
    QPushButton:hover {
        background-color: #45a049;   /* Darker green when hovered */
    }
""")
        
        ##################################
        
        self.add_field_button_proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.add_field_button_proxy.setWidget(self.add_field_button)
        self.add_field_button_proxy.setPos(self.default_margin + 34, self.default_margin + 30)
        
        self.remove_field_button_proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.remove_field_button_proxy.setWidget(self.remove_field_button)
        self.remove_field_button_proxy.setPos(self.default_margin + 49, self.default_margin + 30)
        
        ##################################
        
        self.add_method_button_proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.add_method_button_proxy.setWidget(self.add_method_button)
        self.add_method_button_proxy.setPos(self.default_margin + 48, self.default_margin + 105)
        
        self.remove_method_button_proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.remove_method_button_proxy.setWidget(self.remove_method_button)
        self.remove_method_button_proxy.setPos(self.default_margin + 63, self.default_margin + 105)
        
        ##################################
        
        self.add_field_button.clicked.connect(self.add_field)
        self.remove_field_button.clicked.connect(self.remove_field)
        
        # Connect Method Buttons
        self.add_method_button.clicked.connect(self.add_method)
        self.remove_method_button.clicked.connect(self.remove_method)
        
        #################################################################

        self.methods_label = QtWidgets.QGraphicsTextItem(self)
        self.methods_label.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.methods_label.setPlainText("Methods")  # Set methods label text

        # Create text items for fields and methods
        self.field_text = QtWidgets.QGraphicsTextItem(self)
        self.field_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.field_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.field_text.setPlainText("\n".join(self.field))  # Join fields with newline
        self.field_text.document().contentsChanged.connect(self.update_positions)

        self.methods_text = QtWidgets.QGraphicsTextItem(self)
        self.methods_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.methods_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.methods_text.setPlainText(self.format_methods())  # Format and set methods text
        self.methods_text.document().contentsChanged.connect(self.update_positions)

        # Resizing attributes
        self.is_box_dragged = False  # Flag to indicate if the box is being dragged
        self.is_resizing = False  # Flag to indicate if the box is being resized
        self.current_handle = None  # Currently active resize handle
        self.handle_size = 12  # Size of the resize handle
        self.is_typing = False # Typing flag
        self.create_resize_handles()  # Create resize handle

        # Arrows (connections to other class boxes)
        self.arrows = []  # List to keep track of connected arrows
        self.create_connection_points()  # Create connection points for arrows

        # Update positions of all elements based on the current box size
        self.update_positions()

    #################################################################
    
    def add_field(self):
        field_name, ok = QtWidgets.QInputDialog.getText(None, "Add Field", "Enter field name:")
        if ok and field_name:
            self.field.append(field_name)  # Append the new field name
            self.update_field_text()  # Update the graphical representation of fields

    def remove_field(self):
        if self.field:
            # Show list of current fields for the user to choose which one to delete
            field_names_list = self.field  # Use plain field names
            field_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Field", "Select field to remove:", field_names_list, 0, False)
            if ok and field_name:
                # Remove the field name directly
                self.field.remove(field_name)
                self.update_field_text()  # Update the graphical representation of fields
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No fields to remove.")

    def add_method(self):
        method_name, ok = QtWidgets.QInputDialog.getText(None, "Add Method", "Enter method name:")
        if ok and method_name:
            self.methods.append({method_name + "()" : []})
            self.update_method_text()

    def remove_method(self):
        if len(self.methods) > 0:
            # Extract method names from the methods list
            method_name_list = [list(method.keys())[0] for method in self.methods if method]
            method_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Field", "Select field to remove:", method_name_list, 0, False)
            if ok and method_name:
                # Remove the method name directly
                for each_pair in self.methods:
                    if method_name in each_pair:
                        self.methods.remove(each_pair)
                        break
            self.update_method_text()
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No methods to remove.")
    
    def update_method_text(self):
        """
        Update the displayed text for the method based on the current list of method names.
        """
        self.methods_text.setPlainText(self.format_methods())
        self.update_positions()  # Ensure the positions of all items are updated
        
    def update_field_text(self):
        """
        Update the displayed text for the fields based on the current list of field names.
        """
        self.field_text.setPlainText("\n".join(self.field))  # Update the field text display
        self.update_positions()  # Ensure the positions of all items are updated
            
    #################################################################
    ### MEMBER FUNCTIONS ###

    ## BOX RELATED ##
    
    def start_typing(self):
        """
        Set the flag to indicate typing has started.
        """
        self.is_typing = True

    def format_methods(self):
        """
        Format the methods for display with parameters.

        Returns:
        - str: Formatted methods as a string.
        """
        method_lines = []
        for each_pair in self.methods:
            for method_name, param_list in each_pair.items():
                line = method_name
                method_lines.append(line)
                for each_param in param_list:
                    method_lines.append(f"    {each_param}")  # Indent parameters

        return "\n".join(method_lines)  # Return formatted methods as a string

    def create_resize_handles(self):
        """
        Create resize handles at the bottom-right corner of the class box.
        """
        self.handles = {
            'bottom_right': QtWidgets.QGraphicsEllipseItem(
                0, 0, self.handle_size, self.handle_size, self
            )
        }

        for handle in self.handles.values():
            handle.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))  # Set handle color
            handle.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
            handle.setAcceptHoverEvents(True)  # Enable hover events
            handle.hoverEnterEvent = self.handle_hoverEnterEvent
            handle.hoverLeaveEvent = self.handle_hoverLeaveEvent

    def update_positions(self):
        """
        Update the positions of text items, handles, and connection points.
        """
        # Calculate heights of all text sections
        class_name_height = self.class_name_text.boundingRect().height()
        fields_label_height = self.fields_label.boundingRect().height()
        fields_text_height = self.field_text.boundingRect().height()
        methods_label_height = self.methods_label.boundingRect().height()
        methods_text_height = self.methods_text.boundingRect().height()

        # Set positions of text items relative to each other
        self.class_name_text.setPos(self.default_margin, self.default_margin)
        self.fields_label.setPos(self.default_margin, class_name_height + 2 * self.default_margin)
        self.field_text.setPos(self.default_margin + 10, class_name_height + fields_label_height + 3 * self.default_margin)
        self.methods_label.setPos(self.default_margin, class_name_height + fields_label_height + fields_text_height + 4 * self.default_margin)
        self.methods_text.setPos(self.default_margin + 10, class_name_height + fields_label_height + fields_text_height + methods_label_height + 5 * self.default_margin)
        self.add_field_button_proxy.setPos(self.default_margin + 34, class_name_height + 21)
        self.remove_field_button_proxy.setPos(self.default_margin + 49, class_name_height + 21)
        self.add_method_button_proxy.setPos(self.default_margin + 48, class_name_height + fields_text_height + 62)
        self.remove_method_button_proxy.setPos(self.default_margin + 63, class_name_height + fields_text_height + 62)
        
        # Calculate total height of the box
        total_height = (
            class_name_height + fields_label_height + fields_text_height + methods_label_height + methods_text_height + 6 * self.default_margin
        )

        # Calculate maximum width based on content
        max_width = max(
            self.default_width,
            self.class_name_text.boundingRect().width() + 2 * self.default_margin,
            self.fields_label.boundingRect().width() + 2 * self.default_margin,
            self.field_text.boundingRect().width() + 2 * self.default_margin + 10,
            self.methods_label.boundingRect().width() + 2 * self.default_margin,
            self.methods_text.boundingRect().width() + 2 * self.default_margin + 10,
            self.remove_method_button_proxy.boundingRect().width() + 2 * self.default_margin + 10
        )

        # Update the box size only if not being resized manually
        if not self.is_resizing and not self.is_box_dragged:
            self.setRect(0, 0, max_width, total_height)
            self.user_width = max_width  # Keep track of current user-defined width
            self.user_height = total_height  # Keep track of current user-defined height

        # Update the positions of the separator lines
        self.update_separators()

        # Position the resize handle
        self.handles['bottom_right'].setPos(
            self.rect().width() - self.handle_size // 2,
            self.rect().height() - self.handle_size // 2
        )

        # Update positions of connection points
        self.update_connection_point_positions()

    def update_separators(self):
        """
        Update positions of the separator lines based on current box size.
        """
        rect = self.rect()
        if hasattr(self, 'separator_line1'):
            # Update existing separator lines
            self.separator_line1.setLine(0, self.class_name_text.boundingRect().height() + self.default_margin, rect.width(), self.class_name_text.boundingRect().height() + self.default_margin)  # Line below class name
            self.separator_line2.setLine(0, self.class_name_text.boundingRect().height() + self.fields_label.boundingRect().height() + self.field_text.boundingRect().height() + 3 * self.default_margin, rect.width(), self.class_name_text.boundingRect().height() + self.fields_label.boundingRect().height() + self.field_text.boundingRect().height() + 3 * self.default_margin)  # Line below fields
        else:
            # Create separator lines if they don't exist
            self.separator_line1 = QtWidgets.QGraphicsLineItem(
                0, self.class_name_text.boundingRect().height() + self.default_margin, rect.width(), self.class_name_text.boundingRect().height() + self.default_margin, self
            )
            self.separator_line2 = QtWidgets.QGraphicsLineItem(
                0, self.class_name_text.boundingRect().height() + self.fields_label.boundingRect().height() + self.field_text.boundingRect().height() + 3 * self.default_margin, rect.width(), self.class_name_text.boundingRect().height() + self.fields_label.boundingRect().height() + self.field_text.boundingRect().height() + 3 * self.default_margin, self
            )
            self.separator_line1.setPen(QtGui.QPen(QtCore.Qt.black))
            self.separator_line2.setPen(QtGui.QPen(QtCore.Qt.black))

    #################################################################
    ### CONNECTION POINTS AND ARROWS ###

    def create_connection_points(self):
        """
        Create connection points (dots) for arrow connections.
        """
        self.connection_points = {}  # Dictionary to store positions
        self.connection_point_items = {}  # Dictionary to store the ellipse items

        # Create connection points at 'top', 'bottom', 'left', 'right' of the box
        for key in ['top', 'bottom', 'left', 'right']:
            cp_item = QtWidgets.QGraphicsEllipseItem(-5, -5, 10, 10, self)
            cp_item.setBrush(QtGui.QBrush(QtGui.QColor(0, 150, 0)))  # Dark green color
            cp_item.setPen(QtGui.QPen(QtCore.Qt.black))
            cp_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            cp_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
            self.connection_point_items[key] = cp_item  # Store the item

        self.update_connection_point_positions()  # Position the connection points

    def update_connection_point_positions(self):
        """
        Update positions of the connection point items based on box size.
        """
        rect = self.rect()

        # Calculate positions for 'top', 'bottom', 'left', 'right' points
        self.connection_points = {
            'top': QtCore.QPointF(rect.center().x(), rect.top()),
            'bottom': QtCore.QPointF(rect.center().x(), rect.bottom()),
            'left': QtCore.QPointF(rect.left(), rect.center().y()),
            'right': QtCore.QPointF(rect.right(), rect.center().y())
        }

        # Move the ellipse items to the calculated positions
        self.connection_point_items['top'].setPos(self.connection_points['top'])
        self.connection_point_items['bottom'].setPos(self.connection_points['bottom'])
        self.connection_point_items['left'].setPos(self.connection_points['left'])
        self.connection_point_items['right'].setPos(self.connection_points['right'])

    def getConnectionPoints(self):
        """
        Return the scene positions of the connection points.

        Returns:
        - dict: A dictionary with keys as connection point names and values as QPointF positions.
        """
        scenePoints = {}
        for key, cp_item in self.connection_point_items.items():
            # Adjust position to center of the ellipse
            scenePoints[key] = cp_item.scenePos() + QtCore.QPointF(5, 5)
        return scenePoints

    def addArrow(self, arrow):
        """
        Add an arrow to the list of connected arrows.

        Parameters:
        - arrow (Arrow): The arrow to add.
        """
        self.arrows.append(arrow)

    def removeArrow(self, arrow):
        """
        Remove an arrow from the list of connected arrows.

        Parameters:
        - arrow (Arrow): The arrow to remove.
        """
        if arrow in self.arrows:
            self.arrows.remove(arrow)

    def itemChange(self, change, value):
        """
        Override to update arrows when the class box moves.

        Parameters:
        - change (GraphicsItemChange): The type of change.
        - value (Any): The value associated with the change.

        Returns:
        - Any: The result of the base class itemChange method.
        """
        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            for arrow in self.arrows:
                arrow.updatePosition()
        return super().itemChange(change, value)

    #################################################################
    ## MOUSE RELATED ##

    def handle_hoverEnterEvent(self, event):
        """
        Change cursor to resize when hovering over the resize handle.

        Parameters:
        - event (QGraphicsSceneHoverEvent): The hover event.
        """
        self.setCursor(QtCore.Qt.SizeFDiagCursor)  # Set cursor to diagonal resize
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
                handle.isUnderMouse() for handle in self.handles.values()
            ):
                self.is_box_dragged = True  # Start dragging the box
            elif any(handle.isUnderMouse() for handle in self.handles.values()):
                # Determine which handle is being pressed for resizing
                for handle_name, handle in self.handles.items():
                    if handle.isUnderMouse():
                        self.current_handle = handle_name
                        self.is_resizing = True
                        break
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events for dragging or resizing.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        if self.is_resizing and self.current_handle is not None:
            new_rect = self.rect()

            # Calculate new width and height based on mouse position
            new_width = event.pos().x() - new_rect.x()
            new_height = event.pos().y() - new_rect.y()

            # Set minimum width and height
            min_height = (
                self.class_name_text.boundingRect().height()
                + self.fields_label.boundingRect().height()
                + self.field_text.boundingRect().height()
                + self.methods_label.boundingRect().height()
                + self.methods_text.boundingRect().height()
                + 6 * self.default_margin
            )
           # Calculate the maximum width needed based on the longest text in each section
            longest_string_width = max(
                self.class_name_text.boundingRect().width(),
                self.fields_label.boundingRect().width(),
                self.field_text.boundingRect().width(),
                self.methods_label.boundingRect().width(),
                self.methods_text.boundingRect().width()
            ) + 20  # Add some padding

            # Ensure the box does not overlap with text (min_width now depends on text length)
            if new_width >= longest_string_width:
                new_rect.setWidth(new_width)
            else:
                new_rect.setWidth(longest_string_width)

            if new_height >= min_height:
                new_rect.setHeight(new_height)
            
            # Apply new size and update positions
            self.setRect(new_rect)
            self.update_positions()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to stop dragging or resizing.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        if self.is_box_dragged:
            self.snap_to_grid()  # Snap box to grid
            event.accept()
            self.is_box_dragged = False  # Reset dragging flag
        elif self.is_resizing:
            self.is_resizing = False  # Reset resizing flag
            self.current_handle = None  # Reset current handle

        super().mouseReleaseEvent(event)

    def snap_to_grid(self, current_grid_size=20):
        """
        Snap the class box to the nearest grid position.

        Parameters:
        - current_grid_size (int): The size of the grid to snap to.
        """
        grid_size = current_grid_size * self.transform().m11()  # Adjust for zoom
        pos = self.pos()

        # Calculate new x and y positions
        new_x = round(pos.x() / grid_size) * grid_size
        new_y = round(pos.y() / grid_size) * grid_size

        # Set new position and update
        self.setPos(new_x, new_y)
        self.update_positions()