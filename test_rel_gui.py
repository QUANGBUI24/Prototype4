import sys
import math
from PyQt5 import uic
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem,
    QGraphicsLineItem, QGraphicsTextItem, QGraphicsEllipseItem, QGraphicsItem
)
from PyQt5.QtGui import (
    QPen, QBrush, QPolygonF, QPainter, QColor
)
from PyQt5.QtCore import (
    Qt, QPointF, QLineF
)

# Assuming UMLObserver is defined elsewhere or remove it if not used
# from UML_VIEW.uml_observer import UMLObserver as Observer

##########################################################################
### UMLClassBox ###
class UMLClassBox(QtWidgets.QGraphicsRectItem):
    """
    A representation of a UML class box with editable sections.
    """
    def __init__(self, class_name="ClassName", field=None, methods=None, parent=None):
        super().__init__(parent)

        # Default properties for attributes and methods if not provided
        self.field = field if field is not None else []
        self.methods = methods if methods is not None else []

        # Define the bounding rectangle size
        self.setRect(0, 0, 150, 250)
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
        self.field_text = QtWidgets.QGraphicsTextItem(self)
        self.field_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.field_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.field_text.setPlainText("\n".join(self.field))  # Set attributes text

        self.methods_text = QtWidgets.QGraphicsTextItem(self)
        self.methods_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.methods_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.methods_text.setPlainText(self.format_methods())  # Set methods text
        
        # Create connection points before updating positions
        self.create_connection_points()


        # Resizing attributes
        self.is_box_dragged = False
        self.is_resizing = False
        self.current_handle = None
        self.handle_size = 12  # Size of the corner handles
        self.create_resize_handles()

        # Update positions based on the current box size
        self.update_positions()

        # Flags and variables for connections
        self.arrows = []
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsGeometryChanges
        )

        # Define connection points
        self.connectionPoints = {
            'top': QPointF(self.rect().center().x(), self.rect().top()),
            'bottom': QPointF(self.rect().center().x(), self.rect().bottom()),
            'left': QPointF(self.rect().left(), self.rect().center().y()),
            'right': QPointF(self.rect().right(), self.rect().center().y())
        }

    #################################################################
    ### MEMBER FUNCTIONS ###

    ## BOX RELATED ##

    def format_methods(self):
        """Format the methods for display with parameters."""
        method_lines = []
        for method in self.methods:
            # Start with the method name
            line = method['name']
            method_lines.append(line)  # Add the method name to the list

            # Add parameters with indentation
            for param in method['parameters']:
                method_lines.append(f"    {param}")  # Indent with spaces

        return "\n".join(method_lines)

    def create_resize_handles(self):
        """Create four resize handles at the corners of the class box."""
        # Create four handles for each corner
        self.handles = {
            'bottom_right': QtWidgets.QGraphicsEllipseItem(0, 0, self.handle_size, self.handle_size, self)
        }

        for handle in self.handles.values():
            handle.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))  # Cyan color for visibility
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
        self.field_text.setPos(rect.x() + 15, rect.y() + 55)
        self.methods_text.setPos(rect.x() + 15, rect.y() + 140)

        # Update the positions of the separators based on the text heights
        self.update_separators()

        # Position the resize handles
        self.handles['bottom_right'].setPos(rect.x() + rect.width() - self.handle_size // 2,
                                            rect.y() + rect.height() - self.handle_size // 2)  # Bottom-right

    def update_separators(self):
        """Update the positions of the separator lines based on the current box size and text heights."""
        rect = self.rect()  # Get current rectangle size
        if hasattr(self, 'separator_line1'):
            self.separator_line1.setLine(0, 30, rect.width(), 30)  # Line below class name
            self.separator_line2.setLine(0, 115, rect.width(), 115)  # Line below attributes
        else:
            self.separator_line1 = QtWidgets.QGraphicsLineItem(0, 30, rect.width(), 30, self)  # Line below class name
            self.separator_line2 = QtWidgets.QGraphicsLineItem(0, 115, rect.width(), 115, self)  # Line below attributes

            self.separator_line1.setPen(QtGui.QPen(QtCore.Qt.black))  # Set line color
            self.separator_line2.setPen(QtGui.QPen(QtCore.Qt.black))  # Set line color

    #################################################################
    ## MOUSE RELATED ##

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
                          self.field_text.boundingRect().height() +
                          self.methods_label.boundingRect().height() +
                          self.methods_text.boundingRect().height() + 40)  # Add padding

            # Calculate the maximum width based on the longest string in the labels and text items
            longest_string_width = max(
                self.class_name_text.boundingRect().width(),
                self.fields_label.boundingRect().width(),
                self.field_text.boundingRect().width(),
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

    def snap_to_grid(self, current_grid_size=20):
        """Snap the UML class box to the nearest grid position considering the current zoom level."""
        grid_size = current_grid_size * self.transform().m11()  # Scale grid size by zoom factor
        pos = self.pos()

        # Snap x-coordinate
        new_x = round(pos.x() / grid_size) * grid_size
        # Snap y-coordinate
        new_y = round(pos.y() / grid_size) * grid_size

        # Set the new position
        self.setPos(new_x, new_y)

        # Optionally, update the positions of other elements after snapping
        self.update_positions()

    def addArrow(self, arrow):
        self.arrows.append(arrow)

    def removeArrow(self, arrow):
        if arrow in self.arrows:
            self.arrows.remove(arrow)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for arrow in self.arrows:
                arrow.updatePosition()
        return super().itemChange(change, value)

    def getConnectionPoints(self):
        # Map these points to scene coordinates
        scenePoints = {}
        for key, point in self.connectionPoints.items():
            scenePoints[key] = self.mapToScene(point)
        return scenePoints

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)

        # Draw connection points
        painter.setBrush(QBrush(QColor(0, 150, 0)))  # Dark green color
        radius = 5
        for point in self.connectionPoints.values():
            painter.drawEllipse(point - QPointF(radius, radius), radius, radius)

##########################################################################
### Arrow ###
class Arrow(QGraphicsLineItem):
    def __init__(self, startItem, endItem, startKey, endKey):
        super().__init__()
        self.startItem = startItem
        self.endItem = endItem
        self.startKey = startKey
        self.endKey = endKey
        self.setZValue(2)  # Ensure the arrow is on top
        pen = QPen(Qt.black)
        pen.setWidth(2)
        self.setPen(pen)
        self.arrowSize = 10
        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsFocusable
        )
        # Add this arrow to the items
        self.startItem.addArrow(self)
        self.endItem.addArrow(self)
        self.updatePosition()

    def updatePosition(self):
        # Get updated positions of the connection points
        startPoints = self.startItem.getConnectionPoints()
        endPoints = self.endItem.getConnectionPoints()
        startPoint = startPoints[self.startKey]
        endPoint = endPoints[self.endKey]
        line = QLineF(startPoint, endPoint)
        self.setLine(line)

    def paint(self, painter, option, widget=None):
        painter.setPen(self.pen())
        line = self.line()
        painter.drawLine(line)

        # Draw the arrowhead
        angle = math.atan2(-line.dy(), line.dx())

        arrowP1 = line.p2() - QPointF(
            math.sin(angle + math.pi / 3) * self.arrowSize,
            math.cos(angle + math.pi / 3) * self.arrowSize
        )
        arrowP2 = line.p2() - QPointF(
            math.sin(angle + math.pi - math.pi / 3) * self.arrowSize,
            math.cos(angle + math.pi - math.pi / 3) * self.arrowSize
        )

        arrowHead = QPolygonF([line.p2(), arrowP1, arrowP2])

        painter.setBrush(Qt.black)
        painter.drawPolygon(arrowHead)

##########################################################################
### GridGraphicsView ###
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

        # Variables for arrow drawing
        self.startItem = None
        self.line = None
        self.startPoint = None
        self.startKey = None

    #################################################################
    ## GRID VIEW RELATED ##

    def scale(self, sx, sy):
        """Override the scale method to resize class boxes when zooming."""
        super().scale(sx, sy)

        # Loop through all items in the scene and resize UML class boxes
        for item in self.scene.items():
            if isinstance(item, UMLClassBox):
                # Get the current rect size of the UML class box
                current_rect = item.rect()
                new_width = current_rect.width() * sx
                new_height = current_rect.height() * sy

                # Update the UML class box with new dimensions
                item.setRect(0, 0, new_width, new_height)
                item.update_positions()  # Update positions of text and handles

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

            # Draw origin lines
            origin_pen = QtGui.QPen(QtGui.QColor(255, 0, 0))  # Set to red color for origin lines
            origin_pen.setWidth(2)  # Optional: Increase the line width for visibility
            painter.setPen(origin_pen)

            # Draw horizontal line at y=0
            painter.drawLine(int(rect.left()), 0, int(rect.right()), 0)

            # Draw vertical line at x=0
            painter.drawLine(0, int(rect.top()), 0, int(rect.bottom()))

            # Restore the original pen to continue drawing other elements
            painter.setPen(pen)  # Optional: Reset to original pen for further drawing

    #################################################################
    ## MOUSE RELATED ##

    def wheelEvent(self, event):
        """Handles mouse wheel events to implement zoom in and out functionality using the mouse wheel scroll."""

        # Check if the Ctrl key is pressed
        if event.modifiers() & QtCore.Qt.ControlModifier:
            delta = event.angleDelta().y()

            # Define zoom limits
            zoom_limit = 1.0  # Minimum scale factor
            max_zoom_limit = 5.0  # Maximum scale factor

            # Zoom in and out
            if delta > 0:
                # Wheel scrolled up: Zoom in
                if self.transform().m11() < max_zoom_limit:  # Check if current scale is less than max
                    self.scale(1.1, 1.1)
            elif delta < 0:
                # Wheel scrolled down: Zoom out
                if self.transform().m11() > zoom_limit:  # Check if current scale is greater than min
                    self.scale(0.9, 0.9)

            # Snap the box to the appropriate grid size
            self.update_snap()

            # Request a redraw of the viewport
            self.viewport().update()
            event.accept()
        else:
            # If Ctrl is not pressed, ignore the wheel event
            event.ignore()

    def mousePressEvent(self, event):
        """
        Handles mouse button press events to initiate panning when the middle mouse button is pressed,
        or to start drawing arrows with the right mouse button.
        """
        # Tracking chosen class box
        item = self.itemAt(event.pos())
        if isinstance(item, UMLClassBox):
            self.selected_class = item
        else:
            self.selected_class = None

        if event.button() == QtCore.Qt.MiddleButton:
            # Start panning
            self.is_panning = True
            self.last_mouse_pos = event.pos()
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            event.accept()
        elif event.button() == QtCore.Qt.RightButton:
            # Start drawing an arrow
            scene_pos = self.mapToScene(event.pos())
            items = self.scene.items(scene_pos)
            items = [item for item in items if isinstance(item, UMLClassBox)]
            if items:
                clicked_item = items[0]
                # Find the closest connection point
                connectionPoints = clicked_item.getConnectionPoints()
                min_distance = None
                closest_point = None
                closest_key = None
                for key, point in connectionPoints.items():
                    distance = QLineF(scene_pos, point).length()
                    if min_distance is None or distance < min_distance:
                        min_distance = distance
                        closest_point = point
                        closest_key = key
                self.startItem = clicked_item
                self.startPoint = closest_point
                self.startKey = closest_key

                self.line = QGraphicsLineItem(QLineF(self.startPoint, self.startPoint))
                pen = QPen(Qt.black)
                pen.setWidth(2)
                self.line.setPen(pen)
                self.line.setZValue(2)  # Ensure the line is on top of other items
                self.scene.addItem(self.line)
                event.accept()
            else:
                super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Handles mouse move events to update the scene position when panning is active or drawing arrows.
        """
        if self.is_panning and self.last_mouse_pos is not None:
            # Calculate the distance moved
            delta = event.pos() - self.last_mouse_pos

            # Translate the view accordingly
            self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
            self.translate(delta.x(), delta.y())

            # Update last mouse position
            self.last_mouse_pos = event.pos()

            # Request a redraw of the viewport
            self.viewport().update()

            # Accept the event to indicate it has been handled
            event.accept()
        elif self.line:
            # Update the temporary line during arrow drawing
            new_end = self.mapToScene(event.pos())
            newLine = QLineF(self.startPoint, new_end)
            self.line.setLine(newLine)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Handles mouse button release events to end panning or finish drawing arrows.
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
            items = self.scene.items(scene_pos)
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
                        distance = QLineF(scene_pos, point).length()
                        if min_distance is None or distance < min_distance:
                            min_distance = distance
                            closest_point = point
                            closest_key = key
                    self.endItem = released_item
                    self.endPoint = closest_point
                    self.endKey = closest_key

                    # Check if an arrow from startItem to endItem already exists
                    arrow_exists = any(
                        arrow.startItem == self.startItem and arrow.endItem == self.endItem
                        for arrow in self.startItem.arrows
                    )

                    if arrow_exists:
                        # Don't create a new arrow
                        self.scene.removeItem(self.line)
                        self.line = None
                        # Optionally, you can notify the user
                        QtWidgets.QMessageBox.warning(self, "Duplicate Relationship",
                                                      "An arrow between these classes already exists.")
                    else:
                        # Remove the temporary line
                        self.scene.removeItem(self.line)
                        self.line = None

                        # Create the arrow
                        arrow = Arrow(
                            self.startItem, self.endItem,
                            self.startKey, self.endKey
                        )
                        self.scene.addItem(arrow)
                else:
                    self.scene.removeItem(self.line)
                    self.line = None
            else:
                self.scene.removeItem(self.line)
                self.line = None

            self.startItem = None
            self.endItem = None
            self.startPoint = None
            self.endPoint = None
            self.startKey = None
            self.endKey = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)
            # Request a redraw of the viewport
            self.viewport().update()

    #################################################################
    ## UTILITY ##

    def update_snap(self):
        # Snap all items to the grid after scaling
        for item in self.scene.items():
            if isinstance(item, UMLClassBox):
                item.snap_to_grid()

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
        for item in self.scene.items():
            if isinstance(item, UMLClassBox):
                # Reset to original dimension
                item.setRect(0, 0, 150, 250)
                # Reset others (separators, dot handle)
                item.update_positions()
        self.grid_size = 20
        self.resetTransform()  # Reset the zoom to its original state
        self.centerOn(0, 0)  # Center the view on the origin (initial position)

    def add_class(self):
        # Add a sample UML class box to the scene
        field = ["Field_1", "Field_2"]
        methods = [
            {'name': 'Method_1', 'parameters': ['param_1', 'param_2']},
            {'name': 'Method_2', 'parameters': []}]
        class_box = UMLClassBox(class_name="Class_Name", field=field, methods=methods)
        class_box.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)  # Make the box movable
        class_box.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)  # Make the box selectable
        class_box.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)  # Enable update on move/resize
        self.scene.addItem(class_box)

    def delete_selected_class(self):
        """Deletes the selected class and connected arrows from the scene."""
        if self.selected_class:
            # Remove connected arrows
            for arrow in self.selected_class.arrows[:]:
                arrow.startItem.removeArrow(arrow)
                arrow.endItem.removeArrow(arrow)
                self.scene.removeItem(arrow)
            self.scene.removeItem(self.selected_class)
            self.selected_class = None

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
        self.grid_color = QtGui.QColor(255, 255, 0)  # Cyan for grid lines
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

##########################################################################
### MainWindow ###
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI if you have a .ui file
        # uic.loadUi('prototype_gui.ui', self)

        # Create the grid view and set it as the central widget
        self.grid_view = GridGraphicsView()
        self.setCentralWidget(self.grid_view)

        #################################################################
        ### BUTTONS ###

        # Create toolbars and actions if not using a UI file
        toolbar = self.addToolBar("Main Toolbar")

        ## GRID/VIEW BUTTONS ##
        self.toggle_grid_action = QtWidgets.QAction("Toggle Grid", self)
        self.toggle_grid_action.setCheckable(True)
        self.toggle_grid_action.setChecked(True)
        self.toggle_grid_action.triggered.connect(self.toggle_grid_method)
        toolbar.addAction(self.toggle_grid_action)

        self.change_grid_color_action = QtWidgets.QAction("Change Grid Color", self)
        self.change_grid_color_action.triggered.connect(self.change_gridColor_method)
        toolbar.addAction(self.change_grid_color_action)

        self.reset_view_action = QtWidgets.QAction("Reset View", self)
        self.reset_view_action.triggered.connect(self.reset_view_method)
        toolbar.addAction(self.reset_view_action)

        self.toggle_mode_action = QtWidgets.QAction("Toggle Mode", self)
        self.toggle_mode_action.triggered.connect(self.toggle_mode_method)
        toolbar.addAction(self.toggle_mode_action)

        ## UML DIAGRAM BUTTONS ##
        self.add_class_action = QtWidgets.QAction("Add Class", self)
        self.add_class_action.triggered.connect(self.add_class_to_diagram)
        toolbar.addAction(self.add_class_action)

        self.delete_class_action = QtWidgets.QAction("Delete Class", self)
        self.delete_class_action.triggered.connect(self.delete_selected_class_from_diagram)
        toolbar.addAction(self.delete_class_action)

    #################################################################
    ### EVENT FUNCTIONS ###

    ## GRID EVENTS ##

    def toggle_grid_method(self, checked):
        # Set the visibility of the grid widget based on the checked state
        self.grid_view.setGridVisible(checked)

    def change_gridColor_method(self):
        # Open a color dialog with the current grid color as the initial color
        color = QtWidgets.QColorDialog.getColor(initial=self.grid_view.grid_color, parent=self,
                                                title="Select Grid Color")
        # If the user selected a valid color, update the grid color
        if color.isValid():
            self.grid_view.setGridColor(color)

    def reset_view_method(self):
        # Reset to original view
        self.grid_view.resetView()

    def toggle_mode_method(self):
        self.grid_view.toggleMode()

    def add_class_to_diagram(self):
        # Call the method to add a UML class to the diagram
        self.grid_view.add_class()

    def delete_selected_class_from_diagram(self):
        # Call the method to delete the selected UML class
        self.grid_view.delete_selected_class()

##########################################################################
### Main Function ###
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("UML Diagram Editor")
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
