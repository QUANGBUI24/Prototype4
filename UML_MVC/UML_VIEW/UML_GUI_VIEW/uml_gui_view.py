###################################################################################################

from PyQt5 import uic
from PyQt5 import QtWidgets
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_grid import GridGraphicsView
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_class_box import UMLClassBox
from UML_MVC.uml_observer import UMLObserver as Observer

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
        self.grid_view = GridGraphicsView(self.interface)
        self.setCentralWidget(self.grid_view)
        self.box = UMLClassBox(self.interface)

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
        #################################################################
        
        self.add_class_action = self.findChild(QtWidgets.QAction, "add_class")
        self.delete_class_action = self.findChild(QtWidgets.QAction, "delete_class")
        self.rename_class_action = self.findChild(QtWidgets.QAction, "rename_class")
        
        self.add_class_action.triggered.connect(self.add_class_gui)
        self.delete_class_action.triggered.connect(self.delete_class_gui)  
        self.rename_class_action.triggered.connect(self.rename_class_gui)
        
        #################################################################
        
        self.add_field_action = self.findChild(QtWidgets.QAction, "add_field")
        self.delete_field_action = self.findChild(QtWidgets.QAction, "delete_field")
        self.rename_field_action = self.findChild(QtWidgets.QAction, "rename_field") 
        
        self.add_field_action.triggered.connect(self.add_field_gui) 
        self.delete_field_action.triggered.connect(self.delete_field_gui) 
        self.rename_field_action.triggered.connect(self.rename_field_gui) 
        
        #################################################################
        
        self.add_method_action = self.findChild(QtWidgets.QAction, "add_method")
        self.delete_method_action = self.findChild(QtWidgets.QAction, "delete_method")
        self.rename_method_action = self.findChild(QtWidgets.QAction, "rename_method")
        
        self.add_method_action.triggered.connect(self.add_method_gui) 
        self.delete_method_action.triggered.connect(self.delete_method_gui) 
        self.rename_method_action.triggered.connect(self.rename_method_gui) 
        
        #################################################################
        
        self.add_param_action = self.findChild(QtWidgets.QAction, "add_param")
        self.delete_param_action = self.findChild(QtWidgets.QAction, "delete_param")
        self.rename_param_action = self.findChild(QtWidgets.QAction, "rename_param")
        self.replace_param_action = self.findChild(QtWidgets.QAction, "replace_param")
        
        self.add_param_action.triggered.connect(self.add_param_gui) 
        self.delete_param_action.triggered.connect(self.delete_param_gui) 
        self.rename_param_action.triggered.connect(self.rename_param_gui) 
        self.replace_param_action.triggered.connect(self.replace_param_gui) 
        
    #################################################################
    ### EVENT FUNCTIONS ###

    ## GRID EVENTS ##

    def toggle_grid_method(self, checked):
        """
        Toggle the visibility of the grid.

        Parameters:
        - checked (bool): Indicates whether the grid should be visible.
        """
        self.grid_view.set_grid_visible(checked)

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
            self.grid_view.set_grid_color(color)

    def reset_view_method(self):
        """
        Reset the view to the default state.
        """
        self.grid_view.reset_view()

    def toggle_mode_method(self):
        """
        Switch between light and dark modes.
        """
        self.grid_view.toggle_mode()

    ## UML DIAGRAM EVENTS ##

    def add_class_gui(self):
        """
        Add a new UML class item to the scene.
        """
        self.grid_view.add_class()

    def delete_class_gui(self):
        """
        Delete the selected class or arrow from the diagram.
        """
        self.grid_view.delete_class()
    
    def rename_class_gui(self):
        self.grid_view.rename_class()
        
    def add_field_gui(self):
        self.grid_view.add_field()
        
    def delete_field_gui(self):
        self.grid_view.delete_field()
        
    def rename_field_gui(self):
        self.grid_view.rename_field()
        
    def add_method_gui(self):
        self.grid_view.add_method()
    
    def delete_method_gui(self):
        self.grid_view.delete_method()
        
    def rename_method_gui(self):
        self.grid_view.rename_method()
        
    def add_param_gui(self):
        self.grid_view.add_param()
    
    def delete_param_gui(self):
        self.grid_view.delete_param()
        
    def rename_param_gui(self):
        self.grid_view.rename_param()
        
    def replace_param_gui(self):
        self.grid_view.replace_param()  
        
#################################################################