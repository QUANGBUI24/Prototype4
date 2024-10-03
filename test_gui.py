import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
##################################################################################################################################  

class MainWindow(qtw.QWidget):
    
    #################################################################
    
    def __init__(self):
        super().__init__()
        # Set the main layout as a vertical layout
        main_layout = qtw.QVBoxLayout()
        self.setLayout(main_layout)

        # Create buttons, labels, and input boxes with specified sizes
        self.create_button(main_layout, "Click Me!", lambda: print("Button clicked"), width=100, height=50)
        self.create_label(main_layout, "This is a label", "Sitka Text", 12, width=200, height=30)
        self.create_text_box(main_layout, "input_box", "Enter text here", {}, width=250, height=40)
        combo = self.create_combo_box(main_layout, 
                              ["Hello", "My", "Chicken"],
                              width=150, height=30)
        self.create_spin_box(main_layout, font="Sitka Text", font_size=12, value=10, maximum=50, minimum=10, single_step=10, width=400, height=50)
        self.show()
        
    #################################################################
    
    # Create a button and add it to the specified layout with an optional size
    def create_button(self, layout: qtw.QBoxLayout, button_name: str, action=None, width=None, height=None):
        button = qtw.QPushButton(button_name)
        # Set button size if specified
        self.set_size(button, width, height)
        # Connect the button click event to the action if provided
        if action:
            button.clicked.connect(action)
        # Add the button to the provided layout
        layout.addWidget(button)
        return button

    #################################################################
    
    # Create a label and add it to the specified layout with an optional size
    def create_label(self, layout: qtw.QBoxLayout, label_content: str, font: str = "", font_size: float = 12, width=None, height=None):
        label = qtw.QLabel(label_content)
        label.setFont(qtg.QFont(font, font_size))
        # Set label size if specified
        self.set_size(label, width, height)
        layout.addWidget(label)
        return label

    #################################################################
    
    # Create an input box and add it to the specified layout with optional size and actions
    def create_text_box(self, layout: qtw.QBoxLayout, box_name: str, placeholder_text: str, actions, width=None, height=None):
        box = qtw.QLineEdit()
        box.setObjectName(box_name)
        box.setPlaceholderText(placeholder_text)
        # Set box size if specified
        self.set_size(box, width, height)
        # Ensure actions are provided and each action is callable
        if not isinstance(actions, dict):
            raise TypeError("The actions parameter must be a dictionary of signal-action pairs.")
        # Connect any signals provided in the actions dictionary
        for signal_name, callback in actions.items():
            if not callable(callback):
                raise TypeError(f"The action for signal '{signal_name}' must be a callable function or lambda.")
            # Connect the appropriate signal to the callback
            if signal_name == "textChanged":
                box.textChanged.connect(callback)
            elif signal_name == "editingFinished":
                box.editingFinished.connect(callback)
            elif signal_name == "returnPressed":
                box.returnPressed.connect(callback)
            else:
                raise ValueError(f"Unsupported signal '{signal_name}' for QLineEdit.")
        layout.addWidget(box)
        return box
    
    #################################################################
    
    # Create a combo box and add items to it with optional size, editable state, and insert policy
    def create_combo_box(self, layout: qtw.QBoxLayout, *items, width=None, height=None, editable=False, insert_policy=None):
        combo_box = qtw.QComboBox(self)
        # Make combo box editable if specified
        combo_box.setEditable(editable)
        # Set the insert policy if specified
        if insert_policy:
            combo_box.setInsertPolicy(insert_policy)
        # Add items to the combo box using the helper function
        if items:
            self.add_items_to_combo_box(combo_box, *items)      
        # Set combo box size if specified
        self.set_size(combo_box, width, height)
        # Add the combo box to the provided layout
        layout.addWidget(combo_box)
        return combo_box

    # Helper method to add multiple items to a combo box
    def add_items_to_combo_box(self, combo_box: qtw.QComboBox, *items):
        for item in items:
            # If the item is a tuple, add the first element as text and the rest as user data
            if isinstance(item, tuple):
                text = str(item[0])  # Convert the first element to text for display
                user_data = item[1:] if len(item) > 1 else None
                # Since addItem expects one value for user data, use user_data[0] if there's only one additional value
                if len(user_data) == 1:
                    combo_box.addItem(text, user_data[0])
                else:
                    combo_box.addItem(text, user_data)
            if isinstance(item, list):
                    combo_box.addItems(item)
            else:
                # If item is not a tuple, just add it as the text without any user data
                combo_box.addItem(str(item))
        
    #################################################################
    
    # Create a spin box with optional parameters for value, maximum, minimum, and single step
    def create_spin_box(self, layout: qtw.QBoxLayout, font: str = "", font_size = 12, value=None, maximum=None, minimum=None, single_step=None, prefix=None, suffix=None, width=None, height=None):
        spin_box = qtw.QSpinBox(self)
        # Set initial value if provided
        if value is not None:
            spin_box.setValue(value)
        # Set maximum value if provided
        if maximum is not None:
            spin_box.setMaximum(maximum)
        # Set minimum value if provided
        if minimum is not None:
            spin_box.setMinimum(minimum)
        # Set single step value if provided
        if single_step is not None:
            spin_box.setSingleStep(single_step)
        # Set prefix if provided
        if prefix is not None:
            spin_box.setPrefix(prefix)
        # Set postfix if provided
        if suffix is not None:
            spin_box.setSuffix(suffix)
        self.set_size(spin_box, width, height)
        spin_box.setFont(qtg.QFont(font, font_size))
        # Add spin box to the provided layout
        layout.addWidget(spin_box)
        return spin_box
    
    #################################################################
    
    # Helper to set height and width
    def set_size(self, widget: qtw.QWidget, width=None, height=None):
        if width is not None and height is not None:
            widget.setFixedSize(width, height)
        elif width is not None:
            widget.setFixedWidth(width)
        elif height is not None:
            widget.setFixedHeight(height)

################################################################################################################################## 

app = qtw.QApplication([])
main_window = MainWindow()
app.exec_()
