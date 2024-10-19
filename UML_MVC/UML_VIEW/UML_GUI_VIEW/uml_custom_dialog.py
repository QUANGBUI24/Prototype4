from PyQt5 import QtWidgets

class CustomInputDialog(QtWidgets.QDialog):
    def __init__(self, title="Input Dialog"):
        super().__init__()
        self.setWindowTitle(title)
        self.input_widgets = {}  # Store all input widgets for retrieval
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        
    def add_input(self, label_text, widget_type, options=None):
        """
        Abstract method to add various types of input fields to the dialog.

        Parameters:
        - label_text (str): The label text for the input.
        - widget_type (str): Type of the widget ('combo', 'line', etc.).
        - options (list): Optional list of options for combo boxes.

        Returns:
        - QWidget: The created input widget.
        """
        label = QtWidgets.QLabel(label_text)
        self.layout.addWidget(label)
        
        if widget_type == 'combo':
            combo_box = QtWidgets.QComboBox()
            if options:
                combo_box.addItems(options)
            self.layout.addWidget(combo_box)
            return combo_box
        
        elif widget_type == 'line':
            line_edit = QtWidgets.QLineEdit()
            self.layout.addWidget(line_edit)
            return line_edit

    def rename_field_popup(self, selected_class):
        """
        Example: Creates a dialog for adding a field.
        Uses the abstract method to dynamically create inputs.
        """
        # Create combo box for class name
        old_field_name = self.add_input("Select Field To Rename:", widget_type="combo", options=selected_class.field_name_list)
        new_field_name = self.add_input("Enter New Field Name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets['old_field_name'] = old_field_name
        self.input_widgets['new_field_name'] = new_field_name
        self.add_buttons()
        
    
    def add_buttons(self):
        """
        Helper function to add OK and Cancel buttons.
        """
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)