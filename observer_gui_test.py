# uml_gui.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QListWidget, QVBoxLayout, QPushButton,
    QHBoxLayout, QLineEdit, QMessageBox, QLabel
)
from UML_MANAGER.uml_observer import UMLObserver as Observer
from UML_MANAGER.uml_core_manager import UMLCoreManager

class UMLGui(QWidget, Observer):
    def __init__(self, core_manager: UMLCoreManager):
        super().__init__()
        self.core_manager = core_manager
        self.core_manager._attach(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('UML Class Manager')

        # Main layout
        main_layout = QVBoxLayout()

        # Label
        label = QLabel('Class List:')
        main_layout.addWidget(label)

        # Class list display
        self.class_list_widget = QListWidget()
        main_layout.addWidget(self.class_list_widget)

        # Input field and buttons
        input_layout = QHBoxLayout()
        self.class_name_input = QLineEdit()
        self.class_name_input.setPlaceholderText('Enter class name')
        input_layout.addWidget(self.class_name_input)

        add_button = QPushButton('Add Class')
        add_button.clicked.connect(self.add_class)
        input_layout.addWidget(add_button)

        delete_button = QPushButton('Delete Class')
        delete_button.clicked.connect(self.delete_class)
        input_layout.addWidget(delete_button)

        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)
        self.show()

        # Initial update
        self.update(self.core_manager)

    def add_class(self):
        class_name = self.class_name_input.text().strip()
        if class_name:
            self.core_manager._add_class(class_name, is_loading=False)
            self.class_name_input.clear()
        else:
            QMessageBox.warning(self, 'Input Error', 'Please enter a class name.')

    def delete_class(self):
        selected_items = self.class_list_widget.selectedItems()
        if selected_items:
            class_name = selected_items[0].text()
            self.core_manager._delete_class(class_name)
        else:
            QMessageBox.warning(self, 'Selection Error', 'Please select a class to delete.')

    def update(self, subject: UMLCoreManager, event_type=None, data=None):
        # Clear the list widget
        self.class_list_widget.clear()
        # Populate with updated class list
        class_list = subject._get_class_list()
        for class_name in class_list:
            self.class_list_widget.addItem(class_name)

    def closeEvent(self, event):
        # Detach from the observer list when the window is closed
        self.core_manager._detach(self)
        event.accept()
