###################################################################################################

from typing import List, Dict
from enum import Enum
from UML_MANAGER.uml_core_manager import UMLCoreManager as Manager
from .help_text import show_manual

###################################################################################################

# Global manager #
ProgramManager = Manager()

###################################################################################################
### ENUM VALUES FOR THE INTERFACE ###

class InterfaceOptions(Enum):
    ADD_CLASS = "add_class"
    DELETE_CLASS = "delete_class"
    RENAME = "rename_class"
    ADD_FIELD = "add_field"
    DELETE_FIELD = "delete_field"
    RENAME_FIELD = "rename_field"
    ADD_METHOD = "add_method"
    DELETE_METHOD = "delete_method"
    RENAME_METHOD = "rename_method"
    ADD_PARAM = "add_param"
    DELETE_PARAM = "delete_param"
    RENAME_PARAM = "rename_param"
    ADD_REL = "add_rel"
    DELETE_REL = "delete_rel"
    LIST_CLASS = "list_class"
    CLASS_DETAIL = "class_detail"
    CLASS_REL = "class_rel"
    SAVED_LIST = "saved_list"
    SAVE = "save"
    LOAD = "load"
    DELETE_SAVED = "delete_saved"
    CLEAR_DATA = "clear_data"
    DEFAULT = "default"
    SORT = "sort"
    HELP = "help"
    EXIT = "exit"    
    
###################################################################################################

class UMLCommandLineInterface:
    
    # Constructor for interface #
    def __init__(self):
        pass
    #################################################################
    ### INTERFACE FUNCTIONS THAT CONNECT WITH THE MANAGER ###
    
    ## DATA RELATED FOR GUI ##

    # Get main data #
    def get_main_data(self) -> Dict:
        return ProgramManager._get_main_data()
    
    # Get relationship list #
    def get_relationship_list(self) -> List:
        return ProgramManager._get_relationship_list()
    
    # Get storage manager #
    def get_storage_manager(self):
        return ProgramManager._get_storage_manager()
    
    # Extract and and a list of UML class data #
    """class_data can be retrieved using get_main_data()
       main_data =  get_main_data()
       class_data = main_data["classes"]
    """
    def extract_class_data(self, class_data: List[Dict]) -> List: 
        return ProgramManager._extract_class_data(class_data)
    
    ## CLASS RELATED ##
    
    # Add class interface #
    def add_class(self, class_name: str):
        ProgramManager._add_class(class_name, is_loading=False)
        
    # Delete class interface #
    def delete_class(self, class_name: str):
        ProgramManager._delete_class(class_name, is_loading=False)
        
    # Rename class interface #
    def rename_class(self, current_name: str, new_name: str):
        ProgramManager._rename_class(current_name, new_name, is_loading=False)
        
    ## ATTRIBUTE RELATED ##
    
    # Add attribute interface #
    def add_attribute(self, class_name: str, attribute_name: str):
        ProgramManager._add_field(class_name, attribute_name, is_loading=False)
        
    # Delete attribute interface #
    def delete_attribute(self, class_name: str, attribute_name: str):
        ProgramManager._delete_field(class_name, attribute_name, is_loading=False)
    
    # Rename attribute interface #
    def rename_attribute(self, class_name: str, current_attribute_name: str, new_attribute_name: str):
        ProgramManager._rename_field(class_name, current_attribute_name, new_attribute_name, is_loading=False)
        
    ## METHOD RELATED ##
    
    # Add method interface #
    def add_method(self, class_name: str, method_name: str):
        ProgramManager._add_method(class_name, method_name, is_loading=False)
    
    # Delete method interface #
    def delete_method(self, class_name: str, method_name: str):
        ProgramManager._delete_method(class_name, method_name, is_loading=False)
        
    # Rename method interface #
    def rename_method(self, class_name: str, current_method_name: str, new_method_name: str):
        ProgramManager._rename_method(class_name, current_method_name, new_method_name, is_loading=False)
        
    ## PARAMETER RELATED ##
    
    # Add parameter #
    def add_parameter(self, class_name: str, method_name: str, parameter_name: str):
        ProgramManager._add_parameter(class_name, method_name, parameter_name, is_loading=False)
        
    # Delete parameter #
    def delete_parameter(self, class_name: str, method_name: str, parameter_name: str):
        ProgramManager._delete_parameter(class_name, method_name, parameter_name)
        
    # Rename parameter #
    def rename_parameter(self, class_name: str, method_name: str, current_parameter_name: str, new_parameter_name: str):
        ProgramManager._rename_parameter(class_name, method_name, current_parameter_name, new_parameter_name)
         
    ## RELATIONSHIP RELATED ##
    
    # Add relationship interface #
    def add_relationship(self, source_class_name: str, destination_class_name: str, type: str):
        ProgramManager._add_relationship(source_class_name, destination_class_name, type, is_loading=False)
    
    # Delete relationship interface #
    def delete_relationship(self, source_class_name: str, destination_class_name: str):
        ProgramManager._delete_relationship(source_class_name, destination_class_name, is_loading=False)
    
    ## DISPLAY RELATED ##
    
    # Display saved file list #
    def display_saved_list(self):
        ProgramManager._display_saved_list()
        
    # Display classes #
    def display_classes(self):
        ProgramManager._display_wrapper()
        
    # Display single class #
    def display_single_class(self, class_name: str):
        ProgramManager._display_single_class_detail(class_name)
        
    # Display relationship #
    def display_relationship(self):
        ProgramManager._display_relationship_list()
    
    ## SAVE/LOAD RELATED ##
    
    # Save data #
    def save(self):
        ProgramManager._save()
        
    # Load data #
    def load(self):
        ProgramManager._load()
    
    # Delete saved file #
    def delete_saved_file(self):
        ProgramManager._delete_saved_file()
        
    # Get active file #
    def get_active_file(self) -> str:
        return ProgramManager._get_active_file()
    
    # Saved file name check #
    def saved_file_name_check(self, file_name: str) -> bool:
        return ProgramManager._saved_file_name_check(file_name)
    
    # Clear current active data #
    def clear_current_active_data(self):
        ProgramManager._clear_current_active_data()
    
    # Go back to blank program #
    def end_session(self):
        ProgramManager._end_session()
        
    # Sort class list #
    def sort_class_list(self):
        ProgramManager._sort_class_list()
        
    # Turn off all file statuses when exiting program #
    def exit(self):
        ProgramManager._exit()

    #################################################################   
    def __display_banner(self):
        banner = r"""
        ▗▖ ▗▖▗▖  ▗▖▗▖       ▗▄▄▄▖▗▄▄▄ ▗▄▄▄▖▗▄▄▄▖▗▄▖ ▗▄▄▖ 
        ▐▌ ▐▌▐▛▚▞▜▌▐▌       ▐▌   ▐▌  █  █    █ ▐▌ ▐▌▐▌ ▐▌
        ▐▌ ▐▌▐▌  ▐▌▐▌       ▐▛▀▀▘▐▌  █  █    █ ▐▌ ▐▌▐▛▀▚▖
        ▝▚▄▞▘▐▌  ▐▌▐▙▄▄▖    ▐▙▄▄▖▐▙▄▄▀▗▄█▄▖  █ ▝▚▄▞▘▐▌ ▐▌
                                             
        
            Welcome to the UML Management Interface!
    For more information on commands, type "help" for the manual.
        """
        print(banner)

    def __prompt_menu(self):
       show_manual()

    def main_program_loop(self):
        self.__display_banner()
        while True:
            current_active_file: str = self.get_active_file()
            if current_active_file != "No active file!":
                current_active_file = current_active_file + ".json"
            print(f"\n(Current active file: {current_active_file})")
            print("\n==> ", end="")
            user_input: str = input()
            # Split the input by space
            # Split the input by space
            user_input_component = user_input.split()
            # Get separate command and class name part
            command = user_input_component[0]
            first_param = user_input_component[1] if len(user_input_component) > 1 else None
            second_param = (user_input_component[2] if len(user_input_component) > 2 else None)
            third_param = user_input_component[3] if len(user_input_component) > 3 else None
            fourth_param = user_input_component[4] if len(user_input_component) > 4 else None
            # Start the logic
            #######################################################
            
            # Add class
            if command == InterfaceOptions.ADD_CLASS.value and first_param:
                self.add_class(first_param)
            # Delete class
            elif command == InterfaceOptions.DELETE_CLASS.value and first_param:
                self.delete_class(first_param)
            # Rename class
            elif (
                command == InterfaceOptions.RENAME.value
                and first_param
                and second_param
            ):
                self.rename_class(first_param, second_param)

            #######################################################

            # Add attribute #
            elif (
                command == InterfaceOptions.ADD_FIELD.value
                and first_param
                and second_param
            ):
                self.add_attribute(first_param, second_param)
            # Delete attribute #
            elif (
                command == InterfaceOptions.DELETE_FIELD.value
                and first_param
                and second_param
            ):
                self.delete_attribute(first_param, second_param)
            # Rename attribute #
            elif (
                command == InterfaceOptions.RENAME_FIELD.value
                and first_param
                and second_param
                and third_param
            ):
                self.rename_attribute(first_param, second_param, third_param)

            #######################################################
            
            # Add method #
            elif (
                command == InterfaceOptions.ADD_METHOD.value
                and first_param
                and second_param
            ):
                self.add_method(first_param, second_param)
            # Delete method #
            elif (
                command == InterfaceOptions.DELETE_METHOD.value
                and first_param
                and second_param
            ):
                self.delete_method(first_param, second_param)
            # Rename method #
            elif (
                command == InterfaceOptions.RENAME_METHOD.value
                and first_param
                and second_param
                and third_param
            ):
                self.rename_method(first_param, second_param, third_param)
            
            #######################################################
            
            # Add parameter #
            elif (
                command == InterfaceOptions.ADD_PARAM.value
                and first_param
                and second_param
                and third_param
            ):
                self.add_parameter(first_param, second_param, third_param)
            # Delete parameter #
            elif (
                command == InterfaceOptions.DELETE_PARAM.value
                and first_param
                and second_param
                and third_param
            ):
                self.delete_parameter(first_param, second_param, third_param)
            # Rename parameter #
            elif (
                command == InterfaceOptions.RENAME_PARAM.value
                and first_param
                and second_param
                and third_param
                and fourth_param
            ):
                self.rename_parameter(first_param, second_param, third_param, fourth_param)
            
            #######################################################

            # Add relationship
            elif (
                command == InterfaceOptions.ADD_REL.value
                and first_param
                and second_param
                and third_param
            ):
                self.add_relationship(first_param, second_param, third_param)
            # Delete relationship #
            elif (
                command == InterfaceOptions.DELETE_REL.value
                and first_param
                and second_param
            ):
                self.delete_relationship(first_param, second_param)
                
            #######################################################
                
            # List all the created class names or all class detail #
            elif command == InterfaceOptions.LIST_CLASS.value:
                self.display_classes() 
            # Show the details of the chosen class #
            elif command == InterfaceOptions.CLASS_DETAIL.value and first_param:
                self.display_single_class(first_param)
            # Show the relationship of the chosen class with others #
            elif command == InterfaceOptions.CLASS_REL.value:
                self.display_relationship()
            # Show the list of saved files #
            elif command == InterfaceOptions.SAVED_LIST.value:
                self.display_saved_list()
            # Save the data #
            elif command == InterfaceOptions.SAVE.value:
                self.save()
            # Load the data #
            elif command == InterfaceOptions.LOAD.value:
                self.load()
            # Delete saved file #
            elif command == InterfaceOptions.DELETE_SAVED.value:
                self.delete_saved_file()
            # Clear data in current storage #
            elif command == InterfaceOptions.CLEAR_DATA.value:
                self.clear_current_active_data()
            # Go back to blank program #
            elif command == InterfaceOptions.DEFAULT.value:
                self.end_session()
            # Sort the class list #
            elif command == InterfaceOptions.SORT.value:
                self.sort_class_list()
            # Show the main menu again #
            elif command == InterfaceOptions.HELP.value:
                self.__prompt_menu()
            # Exit the program #
            elif command == InterfaceOptions.EXIT.value:
                break
            else:
                print(f"\nUnknown command '{user_input}'. Type 'help' for a list of commands.")
        self.exit()