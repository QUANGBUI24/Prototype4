import math  # For mathematical calculations (used in Arrow class)
import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets, QtGui, QtCore
from UML_VIEW.uml_observer import UMLObserver as Observer

###################################################################################################

class UMLClassBox(QtWidgets.QGraphicsRectItem):
    """
    A representation of a UML class box with editable sections for class name, fields, and methods.
    Inherits from QGraphicsRectItem to allow graphical representation in a QGraphicsScene.
    """

    #################################################################
    ### CONSTRUCTOR ###

    def __init__(self, class_name="ClassName", field=None, methods=None, parent=None):
        """
        Initializes a new UMLClassBox instance.

        Parameters:
        - class_name (str): The name of the class.
        - field (list): A list of fields (attributes) of the class.
        - methods (list): A list of methods of the class.
        - parent (QGraphicsItem): The parent graphics item.
        """
        super().__init__(parent)

        # Default properties for attributes (fields) and methods if not provided
        self.field = field if field is not None else []
        self.methods = methods if methods is not None else []

        # Define the bounding rectangle size of the class box
        self.setRect(0, 0, 150, 250)
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))  # Set black border
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))  # Set cyan background

        # Create editable text items for the class name, fields, and methods
        self.class_name_text = QtWidgets.QGraphicsTextItem(self)
        self.class_name_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)  # Allow text editing
        self.class_name_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))  # Set text color to black
        self.class_name_text.setPlainText(class_name)  # Set initial class name text

        # Create labels for fields and methods
        self.fields_label = QtWidgets.QGraphicsTextItem(self)
        self.fields_label.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.fields_label.setPlainText("Fields")  # Set fields label text

        self.methods_label = QtWidgets.QGraphicsTextItem(self)
        self.methods_label.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.methods_label.setPlainText("Methods")  # Set methods label text

        # Create text items for fields and methods
        self.field_text = QtWidgets.QGraphicsTextItem(self)
        self.field_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.field_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.field_text.setPlainText("\n".join(self.field))  # Join fields with newline

        self.methods_text = QtWidgets.QGraphicsTextItem(self)
        self.methods_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.methods_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.methods_text.setPlainText(self.format_methods())  # Format and set methods text

        # Resizing attributes
        self.is_box_dragged = False  # Flag to indicate if the box is being dragged
        self.is_resizing = False  # Flag to indicate if the box is being resized
        self.current_handle = None  # Currently active resize handle
        self.handle_size = 12  # Size of the resize handle
        self.create_resize_handles()  # Create resize handle

        # Arrows (connections to other class boxes)
        self.arrows = []  # List to keep track of connected arrows
        self.create_connection_points()  # Create connection points for arrows

        # Update positions of all elements based on the current box size
        self.update_positions()

    #################################################################
    ### MEMBER FUNCTIONS ###

    ## BOX RELATED ##

    def format_methods(self):
        """
        Format the methods for display with parameters.

        Returns:
        - str: Formatted methods as a string.
        """
        method_lines = []
        for method in self.methods:
            line = method['name']
            method_lines.append(line)  # Add the method name

            # Add parameters with indentation
            for param in method['parameters']:
                method_lines.append(f"    {param}")  # Indent parameters

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
        rect = self.rect()  # Get current rectangle dimensions

        # Position text items relative to the box
        self.class_name_text.setPos(rect.x() + 5, rect.y() + 5)
        self.fields_label.setPos(rect.x() + 5, rect.y() + 35)
        self.methods_label.setPos(rect.x() + 5, rect.y() + 120)
        self.field_text.setPos(rect.x() + 15, rect.y() + 55)
        self.methods_text.setPos(rect.x() + 15, rect.y() + 140)

        # Update positions of separator lines
        self.update_separators()

        # Position the resize handle
        self.handles['bottom_right'].setPos(
            rect.x() + rect.width() - self.handle_size // 2,
            rect.y() + rect.height() - self.handle_size // 2
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
            self.separator_line1.setLine(0, 30, rect.width(), 30)  # Line below class name
            self.separator_line2.setLine(0, 115, rect.width(), 115)  # Line below fields
        else:
            # Create separator lines if they don't exist
            self.separator_line1 = QtWidgets.QGraphicsLineItem(
                0, 30, rect.width(), 30, self
            )
            self.separator_line2 = QtWidgets.QGraphicsLineItem(
                0, 115, rect.width(), 115, self
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

            # Calculate minimum height based on text items
            min_height = (
                self.fields_label.y()
                + self.fields_label.boundingRect().height()
                + self.field_text.boundingRect().height()
                + self.methods_label.boundingRect().height()
                + self.methods_text.boundingRect().height()
                + 40  # Additional padding
            )

            # Calculate maximum width based on longest text item
            longest_string_width = (
                max(
                    self.class_name_text.boundingRect().width(),
                    self.fields_label.boundingRect().width(),
                    self.field_text.boundingRect().width(),
                    self.methods_label.boundingRect().width(),
                    self.methods_text.boundingRect().width()
                )
                + 20  # Additional padding
            )

            # Ensure the box does not overlap with text
            if new_width >= longest_string_width:
                new_rect.setWidth(new_width)

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

###################################################################################################

class Arrow(QtWidgets.QGraphicsLineItem):
    """
    Represents an arrow (relationship) between two UMLClassBox instances.
    Inherits from QGraphicsLineItem to draw lines in the scene.
    """

    def __init__(self, startItem, endItem, startKey, endKey):
        """
        Initializes a new Arrow instance.

        Parameters:
        - startItem (UMLClassBox): The starting class box.
        - endItem (UMLClassBox): The ending class box.
        - startKey (str): The connection point key on the starting box.
        - endKey (str): The connection point key on the ending box.
        """
        super().__init__()
        self.startItem = startItem  # Starting class box
        self.endItem = endItem  # Ending class box
        self.startKey = startKey  # Connection point key on starting box
        self.endKey = endKey  # Connection point key on ending box
        self.setZValue(2)  # Ensure the arrow is on top of other items

        # Set pen for drawing the line
        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(2)
        self.setPen(pen)

        self.arrowSize = 10  # Size of the arrowhead

        # Allow the arrow to be selectable and focusable
        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsSelectable |
            QtWidgets.QGraphicsItem.ItemIsFocusable
        )

        # Add this arrow to the connected class boxes
        self.startItem.addArrow(self)
        self.endItem.addArrow(self)

        self.updatePosition()  # Initial position update

    def updatePosition(self):
        """
        Update the position of the arrow based on connected class boxes.
        """
        # Get updated positions of the connection points
        startPoints = self.startItem.getConnectionPoints()
        endPoints = self.endItem.getConnectionPoints()
        startPoint = startPoints[self.startKey]
        endPoint = endPoints[self.endKey]

        # Create a line between the two points
        line = QtCore.QLineF(startPoint, endPoint)
        self.setLine(line)

    def paint(self, painter, option, widget=None):
        """
        Custom paint method to draw the arrow with an arrowhead.

        Parameters:
        - painter (QPainter): The painter object.
        - option (QStyleOptionGraphicsItem): The style options.
        - widget (QWidget): The widget being painted on.
        """
        painter.setPen(self.pen())
        line = self.line()
        painter.drawLine(line)

        # Calculate angle of the line for arrowhead orientation
        angle = math.atan2(-line.dy(), line.dx())

        # Calculate points for the arrowhead polygon
        arrowP1 = line.p2() - QtCore.QPointF(
            math.sin(angle + math.pi / 3) * self.arrowSize,
            math.cos(angle + math.pi / 3) * self.arrowSize
        )
        arrowP2 = line.p2() - QtCore.QPointF(
            math.sin(angle + math.pi - math.pi / 3) * self.arrowSize,
            math.cos(angle + math.pi - math.pi / 3) * self.arrowSize
        )

        # Create the arrowhead polygon
        arrowHead = QtGui.QPolygonF([line.p2(), arrowP1, arrowP2])

        painter.setBrush(QtCore.Qt.black)
        painter.drawPolygon(arrowHead)  # Draw the arrowhead

    def mousePressEvent(self, event):
        """
        Handle mouse press event to allow selection of the arrow.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        self.setSelected(True)  # Select the arrow
        super().mousePressEvent(event)

###################################################################################################

class GridGraphicsView(QtWidgets.QGraphicsView):
    """
    A custom graphics view that displays a grid pattern and handles user interactions.
    Inherits from QGraphicsView.
    """

    #################################################################
    ### CONSTRUCTOR ###

    def __init__(self, parent=None, grid_size=20, color=QtGui.QColor(200, 200, 200)):
        """
        Initializes a new GridGraphicsView instance.

        Parameters:
        - parent (QWidget): The parent widget.
        - grid_size (int): The spacing between grid lines in pixels.
        - color (QColor): The color of the grid lines.
        """
        super().__init__(QtWidgets.QGraphicsScene(parent), parent)

        # Initialize grid properties
        self.grid_visible = True  # Flag to show/hide the grid
        self.is_dark_mode = False  # Flag for light/dark mode
        self.grid_size = grid_size  # Grid spacing
        self.grid_color = color  # Grid line color

        # Set initial view properties
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setSceneRect(-5000, -5000, 10000, 10000)  # Large scene size
        self.setScene(self.scene())

        # Panning state variables
        self.is_panning = False  # Flag to indicate if panning is active
        self.last_mouse_pos = None  # Last mouse position during panning

        # Track selected class or arrow
        self.selected_class = None
        self.selected_arrow = None  # NEW: Track selected arrow

        # Variables for arrow drawing
        self.startItem = None  # Starting class box for arrow
        self.line = None  # Temporary line during arrow drawing
        self.startPoint = None  # Starting point of the arrow
        self.startKey = None  # Starting connection point key

    #################################################################
    ## GRID VIEW RELATED ##

    def scale(self, sx, sy):
        """
        Override scale method to resize class boxes when zooming.

        Parameters:
        - sx (float): Scaling factor in x-direction.
        - sy (float): Scaling factor in y-direction.
        """
        super().scale(sx, sy)

        # Resize UMLClassBox items in the scene
        for item in self.scene().items():
            if isinstance(item, UMLClassBox):
                current_rect = item.rect()
                new_width = current_rect.width() * sx
                new_height = current_rect.height() * sy
                item.setRect(0, 0, new_width, new_height)
                item.update_positions()

    def drawBackground(self, painter, rect):
        """
        Draw the background grid pattern.

        Parameters:
        - painter (QPainter): The painter object.
        - rect (QRectF): The area to be painted.
        """
        # Fill background based on mode
        if self.is_dark_mode:
            painter.fillRect(rect, QtGui.QColor(30, 30, 30))
        else:
            painter.fillRect(rect, QtGui.QColor(255, 255, 255))

        if self.grid_visible:
            # Set pen for grid lines
            pen = QtGui.QPen(self.grid_color)
            pen.setWidth(1)
            painter.setPen(pen)

            # Calculate starting points for grid lines
            left = int(rect.left()) - (int(rect.left()) % self.grid_size)
            top = int(rect.top()) - (int(rect.top()) % self.grid_size)

            # Draw vertical grid lines
            for x in range(left, int(rect.right()), self.grid_size):
                painter.drawLine(x, int(rect.top()), x, int(rect.bottom()))

            # Draw horizontal grid lines
            for y in range(top, int(rect.bottom()), self.grid_size):
                painter.drawLine(int(rect.left()), y, int(rect.right()), y)

            # Draw origin lines
            origin_pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
            origin_pen.setWidth(2)
            painter.setPen(origin_pen)
            painter.drawLine(int(rect.left()), 0, int(rect.right()), 0)  # Horizontal line at y=0
            painter.drawLine(0, int(rect.top()), 0, int(rect.bottom()))  # Vertical line at x=0

            painter.setPen(pen)  # Reset pen

    #################################################################
    ## MOUSE RELATED ##

    def wheelEvent(self, event):
        """
        Handle zoom in/out functionality using the mouse wheel.

        Parameters:
        - event (QWheelEvent): The wheel event.
        """
        if event.modifiers() & QtCore.Qt.ControlModifier:
            delta = event.angleDelta().y()
            zoom_limit = 1.0
            max_zoom_limit = 5.0
            current_scale = self.transform().m11()

            # Zoom in or out based on wheel movement
            if delta > 0 and current_scale < max_zoom_limit:
                self.scale(1.1, 1.1)
            elif delta < 0 and current_scale > zoom_limit:
                self.scale(0.9, 0.9)

            self.update_snap()  # Snap items to grid
            self.viewport().update()
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        """
        Handle mouse press events for panning or starting arrow drawing.

        Parameters:
        - event (QMouseEvent): The mouse event.
        """
        # Determine the item under the mouse cursor
        item = self.itemAt(event.pos())
        if isinstance(item, UMLClassBox):
            self.selected_class = item
            self.selected_arrow = None  # Deselect any arrow
        elif isinstance(item, Arrow):
            self.selected_arrow = item  # Select the arrow
            self.selected_class = None  # Deselect any class
        else:
            self.selected_class = None
            self.selected_arrow = None

        if event.button() == QtCore.Qt.MiddleButton:
            # Start panning
            self.is_panning = True
            self.last_mouse_pos = event.pos()
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            event.accept()
        elif event.button() == QtCore.Qt.RightButton:
            # Start drawing an arrow
            scene_pos = self.mapToScene(event.pos())
            items = self.scene().items(scene_pos)
            items = [item for item in items if isinstance(item, UMLClassBox)]
            if items:
                clicked_item = items[0]
                # Find the closest connection point
                connectionPoints = clicked_item.getConnectionPoints()
                min_distance = None
                closest_point = None
                closest_key = None
                for key, point in connectionPoints.items():
                    distance = QtCore.QLineF(scene_pos, point).length()
                    if min_distance is None or distance < min_distance:
                        min_distance = distance
                        closest_point = point
                        closest_key = key
                self.startItem = clicked_item
                self.startPoint = closest_point
                self.startKey = closest_key

                # Create a temporary line for the arrow
                self.line = QtWidgets.QGraphicsLineItem(
                    QtCore.QLineF(self.startPoint, self.startPoint)
                )
                pen = QtGui.QPen(QtCore.Qt.black)
                pen.setWidth(2)
                self.line.setPen(pen)
                self.line.setZValue(2)
                self.scene().addItem(self.line)
                event.accept()
            else:
                super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events for panning or updating the temporary arrow.

        Parameters:
        - event (QMouseEvent): The mouse event.
        """
        if self.is_panning and self.last_mouse_pos is not None:
            # Panning the view
            delta = event.pos() - self.last_mouse_pos
            self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
            self.translate(delta.x(), delta.y())
            self.last_mouse_pos = event.pos()
            self.viewport().update()
            event.accept()
        elif self.line:
            # Update the temporary arrow line during drawing
            new_end = self.mapToScene(event.pos())
            newLine = QtCore.QLineF(self.startPoint, new_end)
            self.line.setLine(newLine)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to end panning or finish drawing arrows.

        Parameters:
        - event (QMouseEvent): The mouse event.
        """
        if event.button() == QtCore.Qt.MiddleButton and self.is_panning:
            # End panning
            self.is_panning = False
            self.last_mouse_pos = None
            self.setCursor(QtCore.Qt.ArrowCursor)
            event.accept()
        elif event.button() == QtCore.Qt.RightButton and self.line:
            # Finish drawing the arrow
            scene_pos = self.mapToScene(event.pos())
            items = self.scene().items(scene_pos)
            items = [item for item in items if isinstance(item, UMLClassBox)]
            if items:
                released_item = items[0]
                if released_item != self.startItem:
                    # Find the closest connection point on the released item
                    connectionPoints = released_item.getConnectionPoints()
                    min_distance = None
                    closest_point = None
                    closest_key = None
                    for key, point in connectionPoints.items():
                        distance = QtCore.QLineF(scene_pos, point).length()
                        if min_distance is None or distance < min_distance:
                            min_distance = distance
                            closest_point = point
                            closest_key = key
                    self.endItem = released_item
                    self.endPoint = closest_point
                    self.endKey = closest_key

                    # Check if an arrow between these classes already exists
                    arrow_exists = any(
                        arrow.startItem == self.startItem and arrow.endItem == self.endItem
                        for arrow in self.startItem.arrows
                    )

                    if arrow_exists:
                        # Don't create a duplicate arrow
                        self.scene().removeItem(self.line)
                        self.line = None
                        QtWidgets.QMessageBox.warning(
                            self, "Duplicate Relationship",
                            "An arrow between these classes already exists."
                        )
                    else:
                        # Remove the temporary line and create the arrow
                        self.scene().removeItem(self.line)
                        self.line = None
                        arrow = Arrow(
                            self.startItem, self.endItem,
                            self.startKey, self.endKey
                        )
                        self.scene().addItem(arrow)
                else:
                    # Same item clicked; remove temporary line
                    self.scene().removeItem(self.line)
                    self.line = None
            else:
                # No item under cursor; remove temporary line
                self.scene().removeItem(self.line)
                self.line = None

            # Reset variables
            self.startItem = None
            self.endItem = None
            self.startPoint = None
            self.endPoint = None
            self.startKey = None
            self.endKey = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)
            self.viewport().update()

    def keyPressEvent(self, event):
        """
        Handle key press events (e.g., Delete key to remove items).

        Parameters:
        - event (QKeyEvent): The key event.
        """
        if event.key() == QtCore.Qt.Key_Delete:
            self.delete_selected_item()
        else:
            super().keyPressEvent(event)

    #################################################################
    ## UTILITY FUNCTIONS ##

    def delete_selected_item(self):
        """
        Delete the selected class or arrow from the scene.
        """
        if self.selected_class:
            # Remove connected arrows first
            for arrow in self.selected_class.arrows[:]:
                arrow.startItem.removeArrow(arrow)
                arrow.endItem.removeArrow(arrow)
                self.scene().removeItem(arrow)
            # Remove the class box
            self.scene().removeItem(self.selected_class)
            self.selected_class = None
        elif self.selected_arrow:
            # Remove the arrow
            self.selected_arrow.startItem.removeArrow(self.selected_arrow)
            self.selected_arrow.endItem.removeArrow(self.selected_arrow)
            self.scene().removeItem(self.selected_arrow)
            self.selected_arrow = None

    def update_snap(self):
        """
        Snap all items to the grid after scaling.
        """
        for item in self.scene().items():
            if isinstance(item, UMLClassBox):
                item.snap_to_grid()

    def setGridVisible(self, visible):
        """
        Control the visibility of the grid lines.

        Parameters:
        - visible (bool): If True, the grid is shown; if False, it is hidden.
        """
        self.grid_visible = visible
        self.viewport().update()

    def setGridColor(self, color):
        """
        Update the color of the grid lines.

        Parameters:
        - color (QColor): The new color for the grid lines.
        """
        self.grid_color = color
        self.viewport().update()

    def resetView(self):
        """
        Reset the zoom and position to the initial state.
        """
        for item in self.scene().items():
            if isinstance(item, UMLClassBox):
                item.setRect(0, 0, 150, 250)
                item.update_positions()
        self.grid_size = 20
        self.resetTransform()
        self.centerOn(0, 0)

    def add_class(self):
        """
        Add a sample UML class box to the scene.
        """
        field = ["Field_1", "Field_2"]
        methods = [
            {'name': 'Method_1', 'parameters': ['param_1', 'param_2']},
            {'name': 'Method_2', 'parameters': []}
        ]
        class_box = UMLClassBox(class_name="Class_Name", field=field, methods=methods)
        class_box.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        class_box.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        class_box.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.scene().addItem(class_box)

    def setLightMode(self):
        """
        Set the view to light mode.
        """
        self.grid_color = QtGui.QColor(200, 200, 200)
        self.is_dark_mode = False
        self.viewport().update()
        self.scene().update()

    def setDarkMode(self):
        """
        Set the view to dark mode.
        """
        self.grid_color = QtGui.QColor(255, 255, 0)
        self.is_dark_mode = True
        self.viewport().update()
        self.scene().update()

    def toggleMode(self):
        """
        Toggle between dark mode and light mode.
        """
        if self.is_dark_mode:
            self.setLightMode()
        else:
            self.setDarkMode()

###################################################################################################

class MainWindow(QtWidgets.QMainWindow, Observer):
    """
    Main application window that loads the UI and sets up interactions.
    Inherits from QMainWindow and Observer.
    """

    def __init__(self, interface):
        """
        Initializes a new MainWindow instance.

        Parameters:
        - interface: The interface to communicate with UMLCoreManager.
        """
        super().__init__()
        self.interface = interface  # Interface to communicate with UMLCoreManager

        # Load the UI file to access all UI elements
        uic.loadUi('prototype_gui.ui', self)

        # Create the grid view and set it as the central widget
        self.grid_view = GridGraphicsView()
        self.setCentralWidget(self.grid_view)
        self.box = UMLClassBox()

        #################################################################
        ### BUTTONS SETUP ###

        ## GRID/VIEW BUTTONS ##
        # Find QAction objects from the UI file
        self.toggle_grid_button = self.findChild(QtWidgets.QAction, "toggle_grid")
        self.change_grid_color_button = self.findChild(QtWidgets.QAction, "change_grid_color")
        self.reset_view_button = self.findChild(QtWidgets.QAction, "reset_view")
        self.toggle_mode_button = self.findChild(QtWidgets.QAction, "toggle_mode")

        # Connect QAction signals to slot methods
        self.toggle_grid_button.triggered.connect(self.toggle_grid_method)
        self.change_grid_color_button.triggered.connect(self.change_gridColor_method)
        self.reset_view_button.triggered.connect(self.reset_view_method)
        self.toggle_mode_button.triggered.connect(self.toggle_mode_method)

        ## UML DIAGRAM BUTTONS ##
        # Find QAction objects from the toolbar
        self.add_class_action = self.findChild(QtWidgets.QAction, "add_class")
        self.add_class_action.triggered.connect(self.add_class_to_diagram)
        self.delete_class_action = self.findChild(QtWidgets.QAction, "delete_class")
        self.delete_class_action.triggered.connect(self.delete_selected_item_from_diagram)  # Updated method

    #################################################################
    ### EVENT FUNCTIONS ###

    ## GRID EVENTS ##

    def toggle_grid_method(self, checked):
        """
        Toggle the visibility of the grid.

        Parameters:
        - checked (bool): Indicates whether the grid should be visible.
        """
        self.grid_view.setGridVisible(checked)

    def change_gridColor_method(self):
        """
        Open a color dialog to select a new grid color.
        """
        color = QtWidgets.QColorDialog.getColor(
            initial=self.grid_view.grid_color,
            parent=self,
            title="Select Grid Color"
        )
        if color.isValid():
            self.grid_view.setGridColor(color)

    def reset_view_method(self):
        """
        Reset the view to the default state.
        """
        self.grid_view.resetView()

    def toggle_mode_method(self):
        """
        Switch between light and dark modes.
        """
        self.grid_view.toggleMode()

    ## UML DIAGRAM EVENTS ##

    def add_class_to_diagram(self):
        """
        Add a new UML class item to the scene.
        """
        self.grid_view.add_class()

    def delete_selected_item_from_diagram(self):
        """
        Delete the selected class or arrow from the diagram.
        """
        self.grid_view.delete_selected_item()

#################################################################
