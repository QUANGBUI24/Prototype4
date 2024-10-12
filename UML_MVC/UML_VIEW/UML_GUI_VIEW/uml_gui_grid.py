###################################################################################################

import os
from PyQt5 import QtWidgets, QtGui, QtCore
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_class_box import UMLClassBox
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_arrow_line import Arrow

###################################################################################################

class GridGraphicsView(QtWidgets.QGraphicsView):
    """
    A custom graphics view that displays a grid pattern and handles user interactions.
    Inherits from QGraphicsView.
    """

    #################################################################
    ### CONSTRUCTOR ###

    def __init__(self, interface, parent=None, grid_size=15, color=QtGui.QColor(200, 200, 200)):
        """
        Initializes a new GridGraphicsView instance.

        Parameters:
        - parent (QWidget): The parent widget.
        - grid_size (int): The spacing between grid lines in pixels.
        - color (QColor): The color of the grid lines.
        """
        super().__init__(QtWidgets.QGraphicsScene(parent), parent)

        # Interface to communicate with UMLCoreManager
        self.interface = interface  
        
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
        self.startItem = None
        self.endItem = None
        self.startPoint = None
        self.endPoint = None
        self.startKey = None
        self.endKey = None
        self.line = None

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
                item.update_box()

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
    ## CLASS OPERATION ##
    def add_class(self, loaded_class_name=None, is_loading=False):
        """
        Add a sample UML class box to the scene.
        """
        if is_loading:
            is_class_added = self.interface.add_class(loaded_class_name)
            if is_class_added:
                class_box = UMLClassBox(self.interface, class_name=loaded_class_name)
                self.scene().addItem(class_box)
        else:
            # Display a dialog asking the user for the new class name
            input_class_name, ok = QtWidgets.QInputDialog.getText(None, "Add Class", "Enter class name:")
            if ok and input_class_name:
                is_class_added = self.interface.add_class(input_class_name)
                if is_class_added:
                    class_box = UMLClassBox(self.interface, class_name=input_class_name)
                    self.scene().addItem(class_box)
                else:
                    QtWidgets.QMessageBox.warning(None, "Warning", f"Class '{input_class_name}' has already existed!")
            
    def delete_class(self):
        """
        Delete the selected class or arrow from the scene.
        """  
        if self.selected_class:
            # Remove the class box
            input_class_name = self.selected_class.class_name_text.toPlainText()
            is_class_deleted = self.interface.delete_class(input_class_name)
            if is_class_deleted:
                self.scene().removeItem(self.selected_class)
                self.selected_class = None
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", f"Class '{input_class_name}' has already existed!")
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
        
    def rename_class(self):
        """
        Rename the class displayed in the UML box.

        This method prompts the user to input a new name for the class. 
        If the user confirms and enters a valid name, the class name is updated 
        and the box is refreshed to reflect the new name.
        """
        if self.selected_class:
            # Display a dialog asking the user for the new class name
            old_class_name = self.selected_class.class_name_text.toPlainText()
            new_class_name, ok = QtWidgets.QInputDialog.getText(None, "Rename Class", f"Enter new name for class '{old_class_name}'")
            if ok and new_class_name:
                is_class_renamed = self.interface.rename_class(old_class_name, new_class_name)
                if is_class_renamed:
                    self.selected_class.class_name_text.setPlainText(new_class_name)
                    self.selected_class.update_box()
                else:
                    QtWidgets.QMessageBox.warning(None, "Warning", f"New class name'{new_class_name}' has already existed!")
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", f"Class name'{old_class_name}' does not exist!")
                
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
            
    def add_field(self, loaded_class_name=None, loaded_field_name=None, is_loading=False):
        if is_loading:
            # Find the UML class box by the loaded class name in the scene
            for item in self.scene().items():
                if isinstance(item, UMLClassBox) and item.class_name_text.toPlainText() == loaded_class_name:
                    selected_class_box = item  # Found the class box
                    # Add the field to the found class box
                    is_field_added = self.interface.add_field(loaded_class_name, loaded_field_name)
                    if is_field_added:
                        # Create a text item for the field and add it to the list of the found class box
                        field_text = selected_class_box.create_text_item(loaded_field_name, is_field=True, selectable=True, color=selected_class_box.default_text_color)
                        selected_class_box.field_list[loaded_field_name] = field_text  # Add the field to the internal list
                        selected_class_box.field_name_list.append(loaded_field_name)  # Track the field name in the name list
                        selected_class_box.update_box()  # Update the box to reflect the changes
        else:
            if self.selected_class:
                # Display a dialog asking the user for the new field name
                field_name, ok = QtWidgets.QInputDialog.getText(None, "Add Field", "Enter field name:")
                # If the user confirms and provides a valid name, create and add the field
                if ok and field_name:
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_field_added = self.interface.add_field(selected_class_name, field_name)
                    if is_field_added:
                        # Create a text item for the field and add it to the list
                        field_text = self.selected_class.create_text_item(field_name, is_field=True, selectable=True, color=self.selected_class.default_text_color)
                        self.selected_class.field_list[field_name] = field_text  # Add the field to the internal list
                        self.selected_class.field_name_list.append(field_name)  # Track the field name in the name list
                        self.selected_class.update_box()  # Update the box to reflect the changes
                    else:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Field name '{field_name}' has already existed!")
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
            
    def delete_field(self):
        if self.selected_class:
            if self.selected_class.field_name_list:
                # Display a dialog asking the user to select a field to remove
                field_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Field", "Select field to remove:", self.selected_class.field_name_list, 0, False)
                # If the user confirms, remove the selected field from the class
                if ok and field_name:
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_field_deleted = self.interface.delete_field(selected_class_name, field_name)
                    if is_field_deleted:
                        self.selected_class.field_name_list.remove(field_name)  # Remove from the name list
                        self.selected_class.scene().removeItem(self.selected_class.field_list.pop(field_name))  # Remove the text item from the scene
                        self.selected_class.update_box()  # Update the box to reflect the changes
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "No field selected!")
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
    
    def rename_field(self):
        if self.selected_class:
            if self.selected_class.field_name_list:
                # Display a dialog to choose the field to rename
                old_field_name, ok = QtWidgets.QInputDialog.getItem(None, "Change Field Name", "Select field to change:", self.selected_class.field_name_list, 0, False)
                if ok and old_field_name:
                    # Ask for the new name for the selected field
                    new_field_name, ok = QtWidgets.QInputDialog.getText(None, "Rename Field", f"Enter new name for the field '{old_field_name}':")
                    if ok and new_field_name:
                        selected_class_name = self.selected_class.class_name_text.toPlainText()
                        is_field_renamed = self.interface.rename_field(selected_class_name, old_field_name, new_field_name)
                        if is_field_renamed:
                            # Update the field name in the list and refresh the display
                            if old_field_name in self.selected_class.field_list:
                                self.selected_class.field_list[new_field_name] = self.selected_class.field_list.pop(old_field_name)  # Rename the field in the internal list
                                self.selected_class.field_list[new_field_name].setPlainText(new_field_name)  # Set the new field name
                                self.selected_class.field_name_list[self.selected_class.field_name_list.index(old_field_name)] = new_field_name  # Update the name list
                                self.selected_class.update_box()  # Refresh the box display
                        else:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"New field name '{new_field_name}' has already existed!")
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "No fields to change!")
        else:
            # Show a warning if there are no fields to rename
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
            
    def add_method(self, loaded_class_name=None, loaded_method_name=None, is_loading=False):
        if is_loading:
            # Find the UML class box by the loaded class name in the scene
            for item in self.scene().items():
                if isinstance(item, UMLClassBox) and item.class_name_text.toPlainText() == loaded_class_name:
                    selected_class_box = item  # Found the class box
                    # Add the method to the found class box
                    is_method_added = self.interface.add_method(loaded_class_name, loaded_method_name)
                    if is_method_added:
                        # Create a text item for the method and add it to the list of the found class box
                        method_text = selected_class_box.create_text_item(loaded_method_name + "()", is_method=True, selectable=True, color=selected_class_box.default_text_color)
                        selected_class_box.method_list[loaded_method_name] = method_text  # Add the method to the internal list
                        selected_class_box.method_name_list[loaded_method_name] = []  # Track the method name in the name list
                        if len(selected_class_box.method_name_list) == 1:  # If this is the first method, create a separator
                            selected_class_box.create_separator(is_first=False)
                        selected_class_box.update_box()  # Update the box to reflect the changes
        else:
            if self.selected_class:
                # Display a dialog asking for the new method name
                method_name, ok = QtWidgets.QInputDialog.getText(None, "Add Method", "Enter method name:")

                # If the user confirms and provides a valid method name, add it to the UML box
                if ok and method_name:
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_method_added = self.interface.add_method(selected_class_name, method_name)
                    if is_method_added:
                        method_text = self.selected_class.create_text_item(method_name + "()", is_method=True, selectable=True, color=self.selected_class.default_text_color)
                        self.selected_class.method_list[method_name] = method_text  # Store the method text
                        self.selected_class.method_name_list[method_name] = []  # Track the method's parameters
                        if len(self.selected_class.method_name_list) == 1:  # If this is the first method, create a separator
                            self.selected_class.create_separator(is_first=False)
                        self.selected_class.update_box()  # Update the UML box
                    else:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Method name '{method_name}' has already existed!")
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
    
    def delete_method(self):
        if self.selected_class:
            if self.selected_class.method_list:
                # Ask the user to select a method to remove
                method_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Method", "Select method to remove:", self.selected_class.method_name_list, 0, False)

                if ok and method_name:
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_method_deleted = self.interface.delete_method(selected_class_name, method_name)
                    if is_method_deleted:
                        # Remove associated parameters and the method itself
                        for param_name in self.selected_class.method_name_list[method_name]:
                            self.scene().removeItem(self.selected_class.parameter_list.pop(param_name))  # Remove parameter
                        self.selected_class.method_name_list.pop(method_name)  # Remove from method list
                        self.scene().removeItem(self.selected_class.method_list.pop(method_name))  # Remove the method text
                        self.selected_class.update_box()  # Refresh the UML box
            else:
                # Show a warning if there are no methods to remove
                QtWidgets.QMessageBox.warning(None, "Warning", "No methods to remove!")
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
    
    def rename_method(self):
        if self.selected_class:
            # Prompt the user to select the method to rename
            old_method_name, ok = QtWidgets.QInputDialog.getItem(None, "Change Method Name", "Select method to change:", self.selected_class.method_name_list, 0, False)

            if ok and old_method_name:
                # Prompt for the new name
                new_method_name, ok = QtWidgets.QInputDialog.getText(None, "Rename Method", f"Enter new name for the method '{old_method_name}':")
                
                if ok and new_method_name:
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_method_renamed = self.interface.rename_method(selected_class_name, old_method_name, new_method_name)
                    if is_method_renamed:
                        # Update the method name and refresh the UI
                        if old_method_name in self.selected_class.method_list:
                            self.selected_class.method_list[new_method_name] = self.selected_class.method_list.pop(old_method_name)  # Update the method name in the list
                            self.selected_class.method_list[new_method_name].setPlainText(new_method_name + "()")  # Set the new name in the UML box
                            self.selected_class.method_name_list[new_method_name] = self.selected_class.method_name_list.pop(old_method_name)  # Track the change
                            self.selected_class.update_box()  # Refresh the UML box display
                    else:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"New method name '{new_method_name}' has already existed!")
        else:
            # Show a warning if there are no fields to rename
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
            
    def add_param(self,loaded_class_name=None, loaded_method_name=None, loaded_param_name=None, is_loading=False):
        if is_loading:
            # Find the UML class box by the loaded class name in the scene
            for item in self.scene().items():
                if isinstance(item, UMLClassBox) and item.class_name_text.toPlainText() == loaded_class_name:
                    selected_class_box = item  # Found the class box
                    is_param_added = self.interface.add_parameter(loaded_class_name, loaded_method_name, loaded_param_name)
                    if is_param_added:
                        # Add the parameter to the selected method and update the UML box
                        param_text = selected_class_box.create_text_item(loaded_param_name , is_parameter=True, selectable=True, color=selected_class_box.default_text_color)
                        selected_class_box.method_name_list[loaded_method_name].append(loaded_param_name)  # Track the parameter
                        selected_class_box.parameter_list[loaded_param_name] = param_text  # Store the parameter text
                        selected_class_box.parameter_name_list.append(loaded_param_name)  # Add to the list of parameter names
                        selected_class_box.update_box()  # Update the UML box
        else:
            if self.selected_class:
                if self.selected_class.method_list:
                    # Ask the user to choose a method to add a parameter to
                    method_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Method Name", "Select method to add parameter:", list(self.selected_class.method_name_list.keys()), 0, False)
                    if ok and method_name:
                        # Ask for the parameter name
                        param_name, ok = QtWidgets.QInputDialog.getText(None, "Add Parameter", "Enter parameter name:")
                        if ok and param_name:
                            selected_class_name = self.selected_class.class_name_text.toPlainText()
                            is_param_added = self.interface.add_parameter(selected_class_name, method_name, param_name)
                            if is_param_added:
                                # Add the parameter to the selected method and update the UML box
                                param_text = self.selected_class.create_text_item(param_name , is_parameter=True, selectable=True, color=self.selected_class.default_text_color)
                                self.selected_class.method_name_list[method_name].append(param_name)  # Track the parameter
                                self.selected_class.parameter_list[param_name] = param_text  # Store the parameter text
                                self.selected_class.parameter_name_list.append(param_name)  # Add to the list of parameter names
                                self.selected_class.update_box()  # Update the UML box
                            else:
                                QtWidgets.QMessageBox.warning(None, "Warning", f"New parameter name '{param_name}' has already existed!")
                else:
                    # Show a warning if there are no methods available
                    QtWidgets.QMessageBox.warning(None, "Warning", "No methods to choose!")
            else:
                # Show a warning if there are no methods available
                QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
    
    def delete_param(self):
        if self.selected_class:
            if self.selected_class.method_name_list:
                # Ask the user to choose a method to remove a parameter from
                method_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Method Name", "Select method to remove parameter:", 
                                                                 list(self.selected_class.method_name_list.keys()), 0, False)
                if ok and method_name:
                    # Check if the selected method has parameters
                    if self.selected_class.method_name_list[method_name]:
                        # Ask the user to choose the parameter to remove
                        param_name, ok = QtWidgets.QInputDialog.getItem(None, "Delete Parameter", "Choose parameter name to remove:", 
                                                                        self.selected_class.method_name_list[method_name], 0, False)
                        if ok and param_name:
                            selected_class_name = self.selected_class.class_name_text.toPlainText()
                            is_param_deleted = self.interface.delete_parameter(selected_class_name, method_name, param_name)
                            if is_param_deleted:
                                # Remove the parameter and update the UML box
                                self.selected_class.method_name_list[method_name].remove(param_name)  # Remove from method's parameter list
                                self.selected_class.parameter_name_list.remove(param_name)  # Remove from the global parameter list
                                self.scene().removeItem(self.selected_class.parameter_list.pop(param_name))  # Remove from the scene
                                self.selected_class.update_box()  # Refresh the UML box
                            else:
                                QtWidgets.QMessageBox.warning(None, "Warning", "No parameters to choose!")
                    else:
                        # Show a warning if there are no parameters to remove
                        QtWidgets.QMessageBox.warning(None, "Warning", "No parameters to choose!")
            else:
                # Show a warning if there are no methods available
                QtWidgets.QMessageBox.warning(None, "Warning", "No methods to choose!")
        else:
            # Show a warning if there are no class selected
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
            
    
    def rename_param(self):
        if self.selected_class:
            if self.selected_class.method_name_list:
                # Ask the user to choose a method containing the parameter
                method_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Method Name", "Select method:", list(self.selected_class.method_name_list.keys()), 0, False)
                if ok and method_name:
                    # Check if the selected method has parameters
                    if self.selected_class.method_name_list[method_name]:
                        # Ask the user to choose the parameter to rename
                        old_param_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Parameter", "Choose parameter name to rename:", 
                                                                        self.selected_class.method_name_list[method_name], 0, False)
                        if ok and old_param_name:
                            # Ask for the new parameter name
                            new_param_name, ok = QtWidgets.QInputDialog.getText(None, "Rename Parameter", "Enter new parameter name:")
                            if ok and new_param_name:
                                selected_class_name = self.selected_class.class_name_text.toPlainText()
                                is_param_renamed = self.interface.rename_parameter(selected_class_name, method_name, old_param_name, new_param_name)
                                if is_param_renamed:
                                    # Update the parameter name and refresh the UML box
                                    param_list = self.selected_class.method_name_list[method_name]
                                    param_list[param_list.index(old_param_name)] = new_param_name  # Update in the method's parameter list
                                    self.selected_class.parameter_list[new_param_name] = self.selected_class.parameter_list.pop(old_param_name)  # Update the parameter list
                                    self.selected_class.parameter_list[new_param_name].setPlainText(new_param_name)  # Set the new name in the UI
                                    self.selected_class.parameter_name_list[self.selected_class.parameter_name_list.index(old_param_name)] = new_param_name  # Track the change
                                    self.selected_class.update_box()  # Refresh the UML box
                                else:
                                    QtWidgets.QMessageBox.warning(None, "Warning", f"New param name '{new_param_name}' has already existed!")
                    else:
                        # Show a warning if there are no parameters to rename
                        QtWidgets.QMessageBox.warning(None, "Warning", "No parameters to choose.")
            else:
                # Show a warning if there are no methods available
                QtWidgets.QMessageBox.warning(None, "Warning", "No methods to choose.")
        else:
            # Show a warning if there are no class selected
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
    
    def replace_param(self):
        if self.selected_class:
            # Ensure there are methods to choose from
            if self.selected_class.method_name_list:
                # Select the method to replace parameters for
                method_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Method Name", 
                                                             "Select method to replace parameters:", 
                                                             list(self.selected_class.method_name_list.keys()), 0, False)
                if ok and method_name:
                    # Prompt user to enter the new parameters as a comma-separated string
                    param_string, ok = QtWidgets.QInputDialog.getText(None, "Replace Parameters", 
                                                                  "Enter new parameters (comma-separated):")
                    if ok and param_string:
                        # Split the input string by commas to form a list of parameters
                        new_param_list = [param.strip() for param in param_string.split(",") if param.strip()]
                        # Check for duplicate parameter names
                        unique_param_names = list(set(new_param_list))
                        if len(unique_param_names) != len(new_param_list):
                            duplicates = [param for param in new_param_list if new_param_list.count(param) > 1]
                            QtWidgets.QMessageBox.warning(None, "Warning", f"New list contain duplicate{duplicates}!")
                        else:
                            selected_class_name = self.selected_class.class_name_text.toPlainText()
                            is_param_list_replaced = self.interface.replace_param_list_gui(selected_class_name, method_name, new_param_list)
                            if is_param_list_replaced:
                                # Clear current parameters
                                for param_name in self.selected_class.method_name_list[method_name]:
                                    self.scene().removeItem(self.selected_class.parameter_list.pop(param_name))
                                # Clear the method's parameter list
                                self.selected_class.method_name_list[method_name].clear()
                                # Add new parameters to the method
                                for new_param in new_param_list:
                                    param_text = self.selected_class.create_text_item(new_param, is_parameter=True, selectable=True, color=self.selected_class.default_text_color)
                                    self.selected_class.method_name_list[method_name].append(new_param)
                                    self.selected_class.parameter_list[new_param] = param_text
                                    self.selected_class.parameter_name_list.append(new_param)
                                # Update the box to reflect changes
                                self.selected_class.update_box()
            else:
                # Display a warning if no methods are available
                QtWidgets.QMessageBox.warning(None, "Warning", "No methods available to replace parameters.")
        else:
            # Show a warning if there are no class selected
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
            
    def open_folder_gui(self):
        """
        Open a file dialog to select a file.
        """
        self.clear_current_scene()
        # Show an open file dialog and store the selected file path
        full_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), "JSON Files (*.json)")
        if not full_path.endswith('.json'):
            QtWidgets.QMessageBox.warning(None, "Warning", "The selected file is not a JSON file. Please select a valid JSON file.")
            return
        if full_path:
            file_base_name = os.path.basename(full_path)
            file_name_only = os.path.splitext(file_base_name)[0]
            self.interface.load_gui(file_name_only, full_path, self)
            
    def save_as_gui(self):
        """
        Open a save file dialog to select a file location for saving.
        """
        full_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", os.getcwd(),"JSON Files (*.json)")
        if not full_path.endswith('.json'):
            QtWidgets.QMessageBox.warning(None, "Warning", "The selected file is not a JSON file. Please select a valid JSON file.")
            return
        if full_path:
            file_base_name = os.path.basename(full_path)
            file_name_only = os.path.splitext(file_base_name)[0]
            self.interface.save_gui(file_name_only, full_path)

    def save_gui(self):
        """
        Save to current active file, if no active file, prompt user to create new json file
        """
        current_active_file_path = self.interface.get_active_file_gui()
        if current_active_file_path == "No active file!":
            self.save_as_gui()
        else:
            file_base_name = os.path.basename(current_active_file_path)
            file_name_only = os.path.splitext(file_base_name)[0]
            self.interface.save_gui(file_name_only, current_active_file_path)
            
    
    def clear_current_scene(self):
        """
        Remove all UMLClassBox items from the scene.
        """
        # Iterate through all items in the scene
        for item in self.scene().items():
            # Check if the item is a UMLClassBox
            if isinstance(item, UMLClassBox):
                # Remove the item from the scene
                self.scene().removeItem(item)
                
    #################################################################
    ## MOUSE RELATED ##

    def contextMenuEvent(self, event):
        """Show context menu when right-clicking on the UMLClassBox"""
        if self.selected_class:
            #################################
            # Create the context menu
            contextMenu = QtWidgets.QMenu()
            
            # Add box color options
            change_box_color_button = contextMenu.addAction("Box Color")
            
            # Add text color options
            change_text_color_button = contextMenu.addAction("Text Color")
            
            # Add a separator before the class options
            contextMenu.addSeparator()
            
            # Add class options
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
            # Connect box color options to box color functions  
            change_box_color_button.triggered.connect(self.change_box_color)
            
            # Connect text color options to box color functions  
            change_text_color_button.triggered.connect(self.change_text_color)
            
            # Connect class options to class functions
            rename_class_button.triggered.connect(self.rename_class)
            
            # Connect field options to field functions
            add_field_button.triggered.connect(self.add_field)
            delete_field_button.triggered.connect(self.delete_field)
            rename_field_button.triggered.connect(self.rename_field)
        
            # Connect method options to method functions
            add_method_button.triggered.connect(self.add_method)
            delete_method_button.triggered.connect(self.delete_method)
            rename_method_button.triggered.connect(self.rename_method)
        
            # Connect parameter options to parameter functions
            add_parameter_button.triggered.connect(self.add_param)
            delete_parameter_button.triggered.connect(self.delete_param)
            rename_parameter_button.triggered.connect(self.rename_param)
            replace_parameter_button.triggered.connect(self.replace_param)

            # Execute the context menu and get the selected action
            contextMenu.exec_(event.globalPos())
            self.selected_class.update_box()
    
    def wheelEvent(self, event):
        """
        Handle zoom in/out functionality using the mouse wheel.

        Parameters:
        - event (QWheelEvent): The wheel event.
        """
        if event.modifiers() & QtCore.Qt.ControlModifier:
            delta = event.angleDelta().y()
            zoom_limit = 0.5
            max_zoom_limit = 10.0
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
            if self.startPoint:
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
            self.delete_class()
            event.accept()
        else:
            super().keyPressEvent(event)


    #################################################################
    ## UTILITY FUNCTIONS ##

    def update_snap(self):
        """
        Snap all items to the grid after scaling.
        """
        for item in self.scene().items():
            if isinstance(item, UMLClassBox):
                item.snap_to_grid()
                
    def change_box_color(self):
        """
        Open a color dialog to select a new box color.
        """
        if self.selected_class:
            # Get the current brush color, or set a default color if not set
            current_color = self.selected_class.brush().color() if self.selected_class.brush().color().isValid() else QtGui.QColor("cyan")
        
            # Open color dialog and pass current color as the initial color
            color = QtWidgets.QColorDialog.getColor(
                initial=current_color, 
                parent=None,  # Set this to your main window
                title="Select Box Color"
            )
        
            # If a valid color is chosen, set the new brush color for the class box
            if color.isValid():
                self.selected_class.setBrush(QtGui.QBrush(color))
                
    def change_text_color(self):
        """
        Open a color dialog to select a new text color and apply it to the selected UML class box's text.
        """
        if self.selected_class:
            # Get the current text color, or set a default color if not set
            current_color = self.selected_class.class_name_text.defaultTextColor() if self.selected_class.class_name_text.defaultTextColor().isValid() else QtGui.QColor("black")
            # Open color dialog and pass the current color as the initial color
            color = QtWidgets.QColorDialog.getColor(
                initial=current_color, 
                parent=None,  # Optionally set this to your main window for modal behavior
                title="Select Text Color"
            )
            # If a valid color is chosen, set the new color for the text
            if color.isValid():
                if self.selected_class.field_list:
                    for field_text in self.selected_class.field_list.values():
                        field_text.setDefaultTextColor(color)
                if self.selected_class.method_list:
                    for method_text in self.selected_class.method_list.values():
                        method_text.setDefaultTextColor(color)
                if self.selected_class.parameter_list:
                    for param_text in self.selected_class.parameter_list.values():
                        param_text.setDefaultTextColor(color)
                self.selected_class.class_name_text.setDefaultTextColor(color)
                # Ensure later added text will use this color too
                self.selected_class.default_text_color = color
                self.selected_class.update_box()

    def set_grid_visible(self, visible):
        """
        Control the visibility of the grid lines.

        Parameters:
        - visible (bool): If True, the grid is shown; if False, it is hidden.
        """
        self.grid_visible = visible
        self.viewport().update()

    def set_grid_color(self, color):
        """
        Update the color of the grid lines.

        Parameters:
        - color (QColor): The new color for the grid lines.
        """
        self.grid_color = color
        self.viewport().update()

    def reset_view(self):
        """
        Reset the zoom and position to the initial state.
        """
        self.grid_size = 15
        self.resetTransform()
        self.centerOn(0, 0)

    def set_light_mode(self):
        """
        Set the view to light mode.
        """
        self.grid_color = QtGui.QColor(200, 200, 200)
        self.is_dark_mode = False
        self.viewport().update()
        self.scene().update()

    def set_dark_mode(self):
        """
        Set the view to dark mode.
        """
        self.grid_color = QtGui.QColor(255, 255, 0)
        self.is_dark_mode = True
        self.viewport().update()
        self.scene().update()

    def toggle_mode(self):
        """
        Toggle between dark mode and light mode.
        """
        if self.is_dark_mode:
            self.set_light_mode()
        else:
            self.set_dark_mode()