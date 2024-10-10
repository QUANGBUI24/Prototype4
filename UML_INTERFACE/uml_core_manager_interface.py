###################################################################################################

from rich.console import Console
from typing import List, Dict
from UML_MODEL.uml_model import UMLModel as Model
from UML_CONTROLLER.uml_controller import UMLController as Controller, InterfaceOptions

###################################################################################################

class UMLInterface:
    
    # Constructor for interface #
    def __init__(self, view):
        # Each interface instance has its own program manager, easier for testing
        self.Console = Console()
        self.View = view
        self.Model = Model(self.View, self.Console)
        self.Controller = Controller(self.Model, view, self.Console)
        
    #################################################################
    ### INTERFACE FUNCTIONS THAT CONNECT WITH THE MANAGER ###
    
    ## OBJECT CREATION ##
    
    # Class creation method interface #
    def create_class(self, class_name: str):
        return self.Model.create_class(class_name)
    
    # Field creation method interface #
    def create_field(self, field_name: str):
        return self.Model.create_field(field_name)
    
    # Method creation method interface #
    def create_method(self, method_name: str):
        return self.Model.create_method(method_name)
    
    # Parameter creation method interface #
    def create_parameter(self, parameter_name: str):
        return self.Model.create_parameter(parameter_name)
    
    # Relationship creation method interface #
    def create_relationship(self, source_class: str, destination_class: str, rel_type: str):
        return self.Model.create_relationship(source_class, destination_class, rel_type)
    
    ## DATA RELATED FOR GUI AND TESTING ##
    
    # Get class list #
    def get_class_list(self):
        return self.Model._get_class_list()
    
    # Get storage manager interface #
    def get_storage_manager(self):
        return self.Model._get_storage_manager()
    
    # Get relationship list interface #
    def get_relationship_list(self) -> List:
        return self.Model._get_relationship_list()

    # Get main data interface #
    def get_main_data(self) -> Dict:
        return self.Model._get_main_data()
    
    # Get view #
    def get_user_view(self):
        return self.Model._get_user_view()
    
    # Extract and and a list of UML class data interface #
    """class_data can be retrieved using get_main_data()
       main_data =  get_main_data()
       class_data = main_data["classes"]
    """
    def extract_class_data(self, class_data: List[Dict]) -> List: 
        return self.Model._extract_class_data(class_data)
    
    # This one is for Testing, you can check whether 
    # Class, Field, Method, or Parameter exist or not
    # Check uml_core_manager.py to see how to use this function
    # You can find it in _add_class, _add_method, _add_parameters, etc.
    def validate_entities(
        self,
        class_name: str = None, 
        field_name: str = None, 
        method_name: str = None, 
        parameter_name: str = None, 
        class_should_exist: bool = None, 
        field_should_exist: bool = None,
        method_should_exist: bool = None, 
        parameter_should_exist: bool = None
    ) -> bool:
        return self.Model._validate_entities(
            class_name, field_name, method_name, parameter_name, 
            class_should_exist, field_should_exist, 
            method_should_exist, parameter_should_exist)
    
    ## CLASS RELATED ##
    
    # Add class interface #
    def add_class(self, class_name: str):
        self.Model._add_class(class_name, is_loading=False)
        
    # Delete class interface #
    def delete_class(self, class_name: str):
        self.Model._delete_class(class_name)
        
    # Rename class interface #
    def rename_class(self, current_name: str, new_name: str):
        self.Model._rename_class(current_name, new_name)
        
    ## FIELD RELATED ##
    
    # Add field interface #
    def add_field(self, class_name: str, field_name: str):
        self.Model._add_field(class_name, field_name, is_loading=False)
        
    # Delete field interface #
    def delete_field(self, class_name: str, field_name: str):
        self.Model._delete_field(class_name, field_name)
    
    # Rename field interface #
    def rename_field(self, class_name: str, current_field_name: str, new_field_name: str):
        self.Model._rename_field(class_name, current_field_name, new_field_name)
        
    ## METHOD RELATED ##
    
    # Add method interface #
    def add_method(self, class_name: str, method_name: str):
        self.Model._add_method(class_name, method_name, is_loading=False)
    
    # Delete method interface #
    def delete_method(self, class_name: str, method_name: str):
        self.Model._delete_method(class_name, method_name)
        
    # Rename method interface #
    def rename_method(self, class_name: str, current_method_name: str, new_method_name: str):
        self.Model._rename_method(class_name, current_method_name, new_method_name)
        
    ## PARAMETER RELATED ##
    
    # Add parameter interface #
    def add_parameter(self, class_name: str, method_name: str, parameter_name: str):
        self.Model._add_parameter(class_name, method_name, parameter_name, is_loading=False)
        
    # Delete parameter interface #
    def delete_parameter(self, class_name: str, method_name: str, parameter_name: str):
        self.Model._delete_parameter(class_name, method_name, parameter_name)
        
    # Rename parameter interface #
    def rename_parameter(self, class_name: str, method_name: str, current_parameter_name: str, new_parameter_name: str):
        self.Model._rename_parameter(class_name, method_name, current_parameter_name, new_parameter_name)
        
    # Replace parameter list interface #
    def replace_param_list(self, class_name: str, method_name: str):
        self.Model._replace_param_list(class_name, method_name)
        
    ## RELATIONSHIP RELATED ##
    
    # Add relationship interface #
    def add_relationship(self, source_class_name: str, destination_class_name: str, type: str):
        self.Model._add_relationship(source_class_name, destination_class_name, type, is_loading=False)
    
    # Delete relationship interface #
    def delete_relationship(self, source_class_name: str, destination_class_name: str):
        self.Model._delete_relationship(source_class_name, destination_class_name)
        
    # Change relationship type interface #
    def change_type(self, source_class_name: str, destination_class_name: str, new_type: str):
        self.Model._change_type(source_class_name, destination_class_name, new_type)
    
    ## DISPLAY RELATED ##
    
    # Display saved file list #
    def display_saved_list(self):
        self.Model._display_saved_list()
        
    # Display classes #
    def display_classes(self, main_data):
        self.View._display_wrapper(main_data)
        
    # Display single class #
    def display_single_class(self, class_name: str):
        self.Model._display_single_class_detail(class_name)
        
    # Display relationship #
    def display_relationship(self):
        self.Model._display_relationship_list()
    
    ## SAVE/LOAD RELATED ##
    
    # Save data #
    def save(self):
        self.Model._save()
        
    # Save data GUI #
    def save_gui(self, file_name, file_path):
        self.Model._save_gui(file_name, file_path)
        
    # Load data #
    def load(self):
        self.Model._load()
    
    # Delete saved file #
    def delete_saved_file(self):
        self.Model._delete_saved_file()
        
    # Get active file #
    def get_active_file(self) -> str:
        return self.Model._get_active_file()
    
    # Saved file name check #
    def saved_file_name_check(self, file_name: str) -> bool:
        return self.Model._saved_file_name_check(file_name)
    
    # Clear current active data #
    def clear_current_active_data(self):
        self.Model._clear_current_active_data()
    
    # Go back to blank program #
    def end_session(self):
        self.Model._end_session()
        
    # Sort class list #
    def sort_class_list(self):
        self.Model._sort_class_list()
        
    # Exit program #
    def exit(self):
        self.Model._exit()
        
    # Keep updating main data #
    def update_main_data_for_every_action(self):
        self.Model._update_main_data_for_every_action()
        
    ## OBSERVER RELATED ##
    
    # Attach 
    def attach_observer(self, observer):
        self.Model._attach_observer(observer)
        
    # Detach
    def detach_observer(self, observer):
        self.Model._detach_observer(observer)
        
    # notify_observer
    def notify_observer(self):
        self.Model._notify_observer()

    #################################################################   
    
    ## USER INTERFACE ##
    
    # Main program #
    def main_program_loop(self):
       # Display a welcome message and help menu
        self.View._prompt_menu()  # Show initial instructions
        while True:
            # Collect input from the user
            current_active_file: str = self.get_active_file()
            if current_active_file != "No active file!":
                current_active_file = current_active_file + ".json"
            self.Console.print(f"\n[bold yellow](Current active file: [bold white]{current_active_file}[/bold white])[/bold yellow]")
            self.Console. print("\n[bold yellow]==>[/bold yellow] ", end="")
            user_input: str = input()  # User provides the input
            user_input_component = user_input.split()  # Split the input by space
            # Parse command and parameters
            if len(user_input_component) == 0:
                continue
            command = user_input_component[0]
            parameters = user_input_component[1:]
            # Show the main menu again #
            if command == InterfaceOptions.HELP.value:
                self.View._prompt_menu()
            # Exit command handling in the interface
            elif command == InterfaceOptions.EXIT.value:
                break
            # Pass command and parameters to ProgramManager for processing
            self.Controller._process_command(command, parameters)
        self.exit()
