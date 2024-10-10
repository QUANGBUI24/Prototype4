###################################################################################################

from rich.console import Console
from typing import List
from UML_CONTROLLER.uml_storage_manager import UMLStorageManager as Storage
from UML_MODEL.uml_model import UMLModel as Model
from UML_ENUM_CLASS.uml_interface_enum import InterfaceOptions

###################################################################################################
   

class UMLController:
    def __init__(self, model, view, console):
        self.__model = model
        self.__user_view = view
        self.__console = console 
        self.__storage_manager: Storage = Storage()
    
    #################################################################
    
    ## HANDLE USER INPUT FOR INTERFACE ##
    
    # Processing main program including user input #
    def _process_command(self, command: str, parameters: List[str]):
        # Paremeter
        first_param = parameters[0] if len(parameters) > 0 else None
        second_param = parameters[1] if len(parameters) > 1 else None
        third_param = parameters[2] if len(parameters) > 2 else None
        fourth_param = parameters[3] if len(parameters) > 3 else None
        # Start the logic
        #######################################################
        
        # Add class
        if command == InterfaceOptions.ADD_CLASS.value and first_param:
            self.__model._add_class(first_param, is_loading=False)
        # Delete class
        elif command == InterfaceOptions.DELETE_CLASS.value and first_param:
            self.__model._delete_class(first_param)
        # Rename class
        elif (
            command == InterfaceOptions.RENAME_CLASS.value
            and first_param
            and second_param
        ):
            self.__model._rename_class(first_param, second_param)

        #######################################################

        # Add parameter #
        elif (
            command == InterfaceOptions.ADD_FIELD.value
            and first_param
            and second_param
        ):
            self.__model._add_field(first_param, second_param, is_loading=False)
        # Delete parameter #
        elif (
            command == InterfaceOptions.DELETE_FIELD.value
            and first_param
            and second_param
        ):
            self.__model._delete_field(first_param, second_param)
        # Rename parameter #
        elif (
            command == InterfaceOptions.RENAME_FIELD.value
            and first_param
            and second_param
            and third_param
        ):
            self.__model._rename_field(first_param, second_param, third_param)

        #######################################################
            
        # Add method #
        elif (
            command == InterfaceOptions.ADD_METHOD.value
            and first_param
            and second_param
        ):
            self.__model._add_method(first_param, second_param, is_loading=False)
        # Delete method #
        elif (
            command == InterfaceOptions.DELETE_METHOD.value
            and first_param
            and second_param
        ):
            self.__model._delete_method(first_param, second_param)
        # Rename method #
        elif (
            command == InterfaceOptions.RENAME_METHOD.value
            and first_param
            and second_param
            and third_param
        ):
            self.__model._rename_method(first_param, second_param, third_param)
            
        #######################################################
            
        # Add parameter #
        elif (
            command == InterfaceOptions.ADD_PARAM.value
            and first_param
            and second_param
            and third_param
        ):
            self.__model._add_parameter(first_param, second_param, third_param, is_loading=False)
        # Delete parameter #
        elif (
            command == InterfaceOptions.DELETE_PARAM.value
            and first_param
            and second_param
            and third_param
        ):
            self.__model._delete_parameter(first_param, second_param, third_param)
        # Rename parameter #
        elif (
            command == InterfaceOptions.RENAME_PARAM.value
            and first_param
            and second_param
            and third_param
            and fourth_param
        ):
            self.__model._rename_parameter(first_param, second_param, third_param, fourth_param)
        # Replace parameter list #
        elif command == InterfaceOptions.REPLACE_PARAM.value and first_param and second_param:
            self.__model._replace_param_list(first_param, second_param)
            
        #######################################################

        # Add relationship
        elif (
            command == InterfaceOptions.ADD_REL.value
        ):
            self.__model._add_relationship_wrapper(is_loading=False)
        # Delete relationship #
        elif (
            command == InterfaceOptions.DELETE_REL.value
            and first_param
            and second_param
        ):
            self.__model._delete_relationship(first_param, second_param)
        # Chang relationship type #
        elif (
            command == InterfaceOptions.TYPE_MOD.value 
            and first_param
            and second_param
            and third_param
        ):
            self.__model._change_type(first_param, second_param, third_param)
                
        #######################################################
                
        # List all the created class names or all class detail #
        elif command == InterfaceOptions.LIST_CLASS.value:
            self.__user_view._display_wrapper(self.__model._get_main_data()) 
        # Show the details of the chosen class #
        elif command == InterfaceOptions.CLASS_DETAIL.value and first_param:
            self.__user_view._display_single_class(first_param, self.__model._get_main_data())
        # Show the relationship of the chosen class with others #
        elif command == InterfaceOptions.CLASS_REL.value:
            self.__user_view._display_relationships(self.__model._get_main_data())
        # Show the list of saved files #
        elif command == InterfaceOptions.SAVED_LIST.value:
            saved_list = self.__storage_manager._get_saved_list()
            self.__user_view._display_saved_list(saved_list)
        # Save the data #
        elif command == InterfaceOptions.SAVE.value:
            self.__model._save()
        # Load the data #
        elif command == InterfaceOptions.LOAD.value:
            self.__model._load()
        # Delete saved file #
        elif command == InterfaceOptions.DELETE_SAVED.value:
            self.__model._delete_saved_file()
        # Clear data in current storage #
        elif command == InterfaceOptions.CLEAR_DATA.value:
            self.__model._clear_current_active_data()
        # Go back to blank program #
        elif command == InterfaceOptions.DEFAULT.value:
            self.__model._end_session()
        # Sort the class list #
        elif command == InterfaceOptions.SORT.value:
            self.__model._sort_class_list()
        else:
            self.__console.print(f"\n[bold red]Unknown command [bold white]'{command}'[/bold white]. Type 'help' for a list of commands.[/bold red]")