###################################################################################################

import os
from rich.console import Console
from typing import Dict, List
from UML_CORE.UML_CLASS.uml_class import UMLClass as Class
from UML_CORE.UML_FIELD.uml_field import UMLField as Field
from UML_CORE.UML_METHOD.uml_method import UMLMethod as Method
from UML_CORE.UML_PARAMETER.uml_parameter import UMLParameter as Parameter
from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship as Relationship
from UML_CONTROLLER.uml_storage_manager import UMLStorageManager as Storage
from UML_ENUM_CLASS.uml_interface_enum import InterfaceOptions

###################################################################################################

class UMLModel:
    
    #################################################################
    
    # UML Class Manager Constructor #
    
    def __init__(self, view, console):    
        self.__console = console   
        self.__user_view = view
        self.__class_list: Dict[str, Class] = {}
        self.__storage_manager: Storage = Storage()
        self.__relationship_list: List[Relationship] = []
        self.__main_data: Dict = {"classes":[], "relationships":[]}
        self._observers = [] # For observer design pattern
            
    #################################################################
      
    # Observer management methods
    def _attach_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def _detach_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers (self, event_type=None, data=None, is_loading=None):
        for observer in self._observers:
            observer._update(event_type, data, is_loading)
    
    #################################################################
        
    # Getters #
        
    def _get_class_list(self) -> Dict[str, Class]:
        return self.__class_list
    
    def _get_storage_manager(self) -> Storage:
        return self.__storage_manager
    
    def _get_relationship_list(self) -> List[Relationship]:
        return self.__relationship_list
    
    def _get_main_data(self) -> Dict:
        return self.__main_data
    
    def _get_user_view(self):
        return self.__user_view
        
    #################################################################
    ### STATIC FUNCTIONS ###

    # Class creation method #
    @staticmethod
    def create_class(class_name: str) -> Class:
        return Class(class_name)
    
    # Field creation method #
    @staticmethod
    def create_field(field_name: str) -> Field:
        return Field(field_name)
    
    # Method creation method #
    @staticmethod
    def create_method(method_name: str) -> Method:
        return Method(method_name)
    
    # Parameter creation method #
    @staticmethod
    def create_parameter(parameter_name: str) -> Parameter:
        return Parameter(parameter_name)
    
    # Relationship creation method #
    @staticmethod
    def create_relationship(source_class: str, destination_class: str, rel_type: str) -> Relationship:
        return Relationship(source_class, destination_class, rel_type)
    
    #################################################################
    ### MEMBER FUNCTIONS ###
    
    ## CLASS RELATED ##
    
    # Add class #
    def _add_class(self, class_name: str, is_loading: bool):
        # Check if class exists or not
        is_class_exist = self._validate_entities(class_name=class_name, class_should_exist=False)
        # If the class has already existed, stop
        if not is_class_exist:
            return
        # Else, add the class
        new_class = self.create_class(class_name)
        self.__class_list[class_name] = new_class
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.ADD_CLASS.value, data={"class_name" : class_name}, is_loading=is_loading)
        
    # Delete class #
    def _delete_class(self, class_name: str):
        # Check if class exists or not
        is_class_exist = self._validate_entities(class_name=class_name, class_should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Else, delete class
        self.__class_list.pop(class_name)
        # Clean up connected relationship
        self.__clean_up_relationship(class_name)
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.DELETE_CLASS.value, data={"class_name" : class_name})
        
    # Rename class #
    def _rename_class(self, current_name: str, new_name: str):
        # Check if we are able to rename
        is_able_to_rename = self.__check_class_rename(current_name, new_name)
        # If not, stop
        if not is_able_to_rename:
            return
        # Update the real class
        class_object = self.__class_list[current_name]
        class_object._set_class_name(new_name) 
        # Update the key
        self.__class_list[new_name] = self.__class_list.pop(current_name)
        # Update name in relationship list
        self.__update_name_in_relationship(current_name, new_name)
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.RENAME_CLASS.value, data={"old_name" : current_name, "new_name" : new_name})
        
    ## FIELD RELATED ##
    
    # Add field #
    def _add_field(self, class_name: str, field_name: str, is_loading: bool):        
        # Check if class and field exist
        is_class_and_field_exist = self._validate_entities(class_name=class_name, field_name=field_name, class_should_exist=True, field_should_exist=False)
        if not is_class_and_field_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get field list
        field_list = class_object._get_class_field_list()
        # Create new field
        new_field = self.create_field(field_name)
        # Add field
        field_list.append(new_field)
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.ADD_FIELD.value, data={"class_name" : class_name, "field_name" : field_name}, is_loading=is_loading)
        
    # Delete field #
    def _delete_field(self, class_name: str, field_name: str):
        # Check if class and field exist
        is_class_and_field_exist = self._validate_entities(class_name=class_name, field_name=field_name, class_should_exist=True, field_should_exist=True)
        if not is_class_and_field_exist:
            return
         # Get class object
        class_object = self.__class_list[class_name]
        # Get field list
        field_list = class_object._get_class_field_list()
        # Get the field
        chosen_field = self.__get_chosen_field_or_method(class_name, field_name, is_field=True)
        # Remove the chosen field 
        field_list.remove(chosen_field)
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.DELETE_FIELD.value, data={"class_name" : class_name, "field_name" : field_name})
        
    # Rename field #
    def _rename_field(self, class_name: str, current_field_name: str, new_field_name: str):
        is_able_to_rename = self.__check_field_or_method_rename(class_name, current_field_name, new_field_name, is_field=True)
        if not is_able_to_rename:
            return
        # Get the field
        chosen_field = self.__get_chosen_field_or_method(class_name, current_field_name, is_field=True)
        chosen_field._set_name(new_field_name)
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.RENAME_FIELD.value, 
                     data={"class_name" : class_name, "old_field_name" : current_field_name, "new_field_name" : new_field_name})
        
    ## METHOD RELATED ##
    
    # Add method #
    def _add_method(self, class_name: str, method_name: str, is_loading: bool):
        # Check if class and method exist or not
        is_class_and_method_exist = self._validate_entities(class_name=class_name, method_name=method_name, class_should_exist=True, method_should_exist=False)
        if not is_class_and_method_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get field list
        method_list = class_object._get_class_method_list()
        # Create new method
        new_method = self.create_method(method_name)
        # Add method
        method_list.append(new_method)
        # Get method and parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        # Add method with empty list of parameter
        method_and_parameter_list[method_name] = [] 
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.ADD_METHOD.value, data={"class_name" : class_name, "method_name" : method_name}, is_loading=is_loading)
        
    # Delete method #
    def _delete_method(self, class_name: str, method_name: str):
        # Check if class and method exist or not
        is_class_and_method_exist = self._validate_entities(class_name=class_name, method_name=method_name, class_should_exist=True, method_should_exist=True)
        if not is_class_and_method_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get method list
        method_list = class_object._get_class_method_list()
        # Get method and parameter list and delete the method from it
        method_and_parameter_list = class_object._get_method_and_parameters_list()
        method_and_parameter_list.pop(method_name)
        # Get the method
        chosen_method = self.__get_chosen_field_or_method(class_name, method_name, is_field=False)
        # Remove the chosen method 
        method_list.remove(chosen_method)
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.DELETE_METHOD.value, data={"class_name" : class_name, "method_name" : method_name})
        
    # Rename method #
    def _rename_method(self, class_name: str, current_method_name: str, new_method_name: str):
        is_able_to_rename = self.__check_field_or_method_rename(class_name, current_method_name, new_method_name, is_field=False)
        if not is_able_to_rename:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get method and parameter list and update the key (method name)
        method_and_parameter_list = class_object._get_method_and_parameters_list()
        method_and_parameter_list[new_method_name] = method_and_parameter_list.pop(current_method_name)
        # Get the method
        chosen_method = self.__get_chosen_field_or_method(class_name, current_method_name, is_field=False)
        chosen_method._set_name(new_method_name)
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.RENAME_METHOD.value,
                     data={"class_name" : class_name, "old_method_name" : current_method_name, "new_method_name" : new_method_name})
        
    ## PARAMETER RELATED ##
    
    # Add parameter #
    def _add_parameter(self, class_name: str, method_name: str, parameter_name: str, is_loading: bool):
        # Check if class, method and its parameter exist or not
        is_class_and_method_and_parameter_exist = self._validate_entities(class_name=class_name, method_name=method_name,parameter_name=parameter_name, class_should_exist=True, method_should_exist=True, parameter_should_exist=False )
        if not is_class_and_method_and_parameter_exist:
            return
        # Get method and parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        # Create parameter
        new_parameter = self.create_parameter(parameter_name)
        # Add new parameter
        method_and_parameter_list[method_name].append(new_parameter) 
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.ADD_PARAM.value,
                     data={"class_name" : class_name, "method_name" : method_name, "param_name" : parameter_name}, is_loading=is_loading)
        
    # Delete parameter #
    def _delete_parameter(self, class_name: str, method_name: str, parameter_name: str):
        # Check if class, method and its parameter exist or not
        is_class_and_method_and_parameter_exist = self._validate_entities(class_name=class_name, method_name=method_name,parameter_name=parameter_name, class_should_exist=True, method_should_exist=True, parameter_should_exist=True )
        if not is_class_and_method_and_parameter_exist:
            return
        # Get method and parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        # Get chosen parameter
        chosen_parameter = self.__get_chosen_parameter(class_name, method_name, parameter_name)
        # Remove the chosen parameter
        method_and_parameter_list[method_name].remove(chosen_parameter)
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.DELETE_PARAM.value, 
                     data={"class_name" : class_name, "method_name" : method_name, "param_name" : parameter_name})
        
    # Rename parameter #
    def _rename_parameter(self, class_name: str, method_name: str, current_parameter_name: str, new_parameter_name: str):
        # Check if class, method and its parameter exist or not
        is_class_and_method_and_current_parameter_exist = self._validate_entities(class_name=class_name, method_name=method_name,parameter_name=current_parameter_name, class_should_exist=True, method_should_exist=True, parameter_should_exist=True )
        if not is_class_and_method_and_current_parameter_exist:
            return
        # Check if new parameter exists or not
        is_new_parameter_exist = self._validate_entities(class_name=class_name, method_name=method_name,parameter_name=new_parameter_name, class_should_exist=True, method_should_exist=True, parameter_should_exist=False )
        # If new parameter exist, stop
        if not is_new_parameter_exist:
            return
        # Get chosen parameter
        chosen_parameter = self.__get_chosen_parameter(class_name, method_name, current_parameter_name)
        chosen_parameter._set_parameter_name(new_parameter_name)
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.RENAME_PARAM.value, 
                     data={"class_name" : class_name, "method_name" : method_name, 
                           "old_param_name" : current_parameter_name, "new_param_name" : new_parameter_name})
        
    # Replace parameter list, fail if class or method does not exist
    def _replace_param_list(self, class_name: str, method_name: str):
        # Check if class and method exist or not
        is_class_and_method_exist = self._validate_entities(class_name=class_name, method_name=method_name, class_should_exist=True, method_should_exist=True)
        if not is_class_and_method_exist:
            return
        # Get new parameter names from the user
        self.__console.print("\n[bold yellow]Enter the names for the new parameter list, each name must be separated by spaces:[/bold yellow]\n\n[bold white]==>[/bold white] ")
        user_input = input()
        new_param_name_list = user_input.split()
        # Check for duplicates in the parameter list
        unique_param_names = list(set(new_param_name_list))
        if len(unique_param_names) != len(new_param_name_list):
            self.__console.print("\n[bold red]Duplicate parameters detected:[/bold red]")
            duplicates = [param for param in new_param_name_list if new_param_name_list.count(param) > 1]
            self.__console.print(f"\n[bold red]Duplicates: [bold white]{set(duplicates)}[/bold white][/bold red]")
            self.__console.print("\n[bold red]Please modify the parameter list manually to ensure uniqueness.[/bold red]")
            return
        # Create parameter objects for the specific method
        new_param_list: List[Parameter] = []
        for param_name in new_param_name_list:
            new_param = self.create_parameter(param_name)
            new_param_list.append(new_param)
        # Replace the parameter list in the specified method
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        method_and_parameter_list[method_name] = new_param_list
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.REPLACE_PARAM.value, 
                     data={"class_name" : class_name, "method_name" : method_name, "new_list" : new_param_list})
        
    ## RELATIONSHIP RELATED ##
    
    # Add relationship wrapper #
    def _add_relationship_wrapper(self, is_loading: bool):
        if len(self.__class_list) == 0:
            self.__console.print("\n[bold red]No class exists![/bold red]")
            return
        self.__console.print("\n[bold yellow]Type [bold white]'<source_class> <destination_class> <type>'[/bold white] or type [bold white]'quit'[/bold white] to return to main menu[/bold yellow]")
        self.__user_view._display_type_enum()
        self.__user_view._display_class_names(self.__main_data)
        self.__user_view._display_relationships(self.__main_data)
        self.__console.print("\n[bold yellow]==>[/bold yellow] ", end="")
        user_input: str = input()
        if user_input == "quit":
            self.__console.print("\n[bold green]Canceled adding relationship[/bold green]")
            return
        # Split the input by space
        user_input_component = user_input.split()
        # Get separate class name part and type part
        source_class_name = user_input_component[0]
        destination_class_name = (user_input_component[1] if len(user_input_component) > 1 else None)
        type = user_input_component[2] if len(user_input_component) > 2 else None
        # Check if user type the correct format
        if source_class_name and destination_class_name and type:
            # Check if source class exists or not
            is_source_class_exist = self.__validate_class_existence(source_class_name, should_exist=True)
            # If the class does not exist, stop
            if not is_source_class_exist:
                return
            # Check if destination class exists or not
            is_destination_class_exist = self.__validate_class_existence(destination_class_name, should_exist=True)
            # If the class does not exist, stop
            if not is_destination_class_exist:
                return
            # Check if the relationship already exist or not
            is_relationship_exist = self.__relationship_exist(source_class_name, destination_class_name)
            if is_relationship_exist:
                self.__console.print(f"\n[bold red]Relation ship between class [bold white]'{source_class_name}'[/bold white] to class [bold white]'{destination_class_name}'[/bold white] has already existed![/bold red]")
                return
            # Checking type, 
            is_type_exist = self.__validate_type_existence(type, should_exist=True)
            if not is_type_exist:
                return
            # If exists, then finally add relationship
            self._add_relationship(source_class_name, destination_class_name, type, is_loading)
        else:
            self.__console.print("\n[bold red]Wrong format! Please try again![/bold red]")
            
    # Add relationship #
    def _add_relationship(self, source_class_name: str, destination_class_name: str, rel_type: str, is_loading: bool):
        # Create new relationship
        new_relationship = self.create_relationship(source_class_name, destination_class_name, rel_type)
        # Add new relationship to the list
        self.__relationship_list.append(new_relationship) 
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.ADD_REL.value, 
                     data={"source" : source_class_name, "dest" : destination_class_name, "type" : rel_type}, 
                     is_loading=is_loading)
        
    # Delete relationship #
    def _delete_relationship(self, source_class_name: str, destination_class_name: str):
        # Check if source class exists or not
        is_source_class_exist = self.__validate_class_existence(source_class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_source_class_exist:
            return
        # Check if destination class exists or not
        is_destination_class_exist = self.__validate_class_existence(destination_class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_destination_class_exist:
            return
        # Check if the relationship already exist or not
        is_relationship_exist = self.__relationship_exist(source_class_name, destination_class_name)
        if not is_relationship_exist:
            self.__console.print(f"\n[bold red]Relation ship between class [bold white]'{source_class_name}'[/bold white] to class [bold white]'{destination_class_name}'[/bold white] does not exist![bold red]")
            return
        # Get chosen relationship
        current_relationship = self.__get_chosen_relationship(source_class_name, destination_class_name)
        # Remove relationship
        self.__relationship_list.remove(current_relationship)
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.DELETE_REL.value, data={"source" : source_class_name, "dest" : destination_class_name})
        
    # Change type #
    def _change_type(self, source_class_name: str, destination_class_name: str, new_type: str):
        # Check if class names are identical or not
        if source_class_name == destination_class_name:
            self.__console.print("\n[bold red]No relationship from a class to itself![/bold red]")
            return
        # Check source class existence
        is_source_class_name_exist = self.__validate_class_existence(source_class_name, should_exist=True)
        if not is_source_class_name_exist:
            return
        # Check destination class existence
        is_destination_class_name_exist = self.__validate_class_existence(destination_class_name, should_exist=True)
        if not is_destination_class_name_exist:
            return
        # Check if new type is identical to current type:
        current_type = self.__get_chosen_relationship_type(source_class_name, destination_class_name)
        if current_type == new_type:
            self.__console.print(f"\n[bold red]New type [bold white]'{new_type}'[/bold white] is identical to the existing type of the current relationship![/bold red]")
            return
        # Check if type already existed or not
        is_type_exist = self.__validate_type_existence(new_type, should_exist=True)
        if not is_type_exist:
            return
        current_relationship = self.__get_chosen_relationship(source_class_name, destination_class_name)
        if current_relationship is None:
            return
        current_relationship._set_type(new_type)
        # Updating main data
        self._update_main_data_for_every_action()
        # Notify observers
        self._notify_observers (event_type=InterfaceOptions.TYPE_MOD.value, data={"source" : source_class_name, "dest" : destination_class_name, "new_type" : new_type})
        
    #################################################################
    ### HELPER FUNCTIONS ###  
    
    ## CLASS RELATED ## 

    # Validate if the class name exists in the class list #
    def __class_exists(self, class_name: str) -> bool:
        return class_name in self.__class_list
    
    # Validate class name based on whether it should exist or not #
    def __validate_class_existence(self, class_name: str, should_exist: bool) -> bool:
        # When class name should exist but it does not
        is_class_name_exist = self.__class_exists(class_name)
        if should_exist and not is_class_name_exist:
            self.__console.print(f"\n[bold red]Class [bold white]'{class_name}'[/bold white] does not exist![/bold red]")
            return False
        # When class name should not exist but it does
        elif not should_exist and is_class_name_exist:
            self.__console.print(f"\n[bold red]Class [bold white]'{class_name}'[/bold white] has already existed![/bold red]")
            return False
        # True in any other cases
        return True

    # Check if we are able to rename class #
    def __check_class_rename(self, current_class_name: str, new_class_name: str) -> bool:
        # Check if current class name exists or not
        is_current_class_name_exist = self.__validate_class_existence(current_class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_current_class_name_exist:
            return False
        # Check if new class name exists or not
        is_new_class_name_exist = self.__validate_class_existence(new_class_name, should_exist=False)
        # If the class has already existed, stop
        if not is_new_class_name_exist:
            return False
        return True
    
    # Clean Up Relationship #
    def __clean_up_relationship(self, class_name: str):
        # Create a new list that excludes relationships with dest or source equal to class_name
        relationship_list = self.__relationship_list
        relationship_list[:] = [
            relationship
            for relationship in relationship_list
            if relationship._get_source_class() != class_name and relationship._get_destination_class() != class_name
        ]
    
    # Update source/destination class name when we rename a class name #
    def __update_name_in_relationship(self, current_name: str, new_name: str):
        # Get relationship list
        relationship_list = self.__relationship_list
        # Loop through the relationship list
        for each_relationship in relationship_list:
            source_name = each_relationship._get_source_class()
            destination_name = each_relationship._get_destination_class()
            if source_name == current_name:
                each_relationship._set_source_class(new_name)
            elif destination_name == current_name:
                each_relationship._set_destination_class(new_name)
                
    # Get method and parameter list of a chosen class #
    def _get_method_and_parameter_list(self, class_name: str) -> Dict[str, List[Parameter]] | None:
        is_class_name_exist = self.__validate_class_existence(class_name, should_exist=True)
        if not is_class_name_exist:
            return None
        return self.__class_list[class_name]._get_method_and_parameters_list()
    
    ## FIELD AND METHOD RELATED ##
    
    # Check field/method name exist or not #
    def __field_or_method_exist(self, class_name: str, input_name: str, is_field: bool) -> bool:
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Select the correct list based on is_field
        if is_field:
            general_list = class_object._get_class_field_list()
        else:
            general_list = class_object._get_class_method_list()
        # Loop through the list to find the field or method name 
        for element in general_list:
            current_name = element._get_name()
            # If exists, return true
            if current_name == input_name:
                return True
        return False
    
    # Validate field name based on whether it should exist or not #
    def __validate_field_existence(self, class_name: str,  field_name: str, should_exist: bool) -> bool:
        # When field name should exist but it does not
        is_field_name_exist = self.__field_or_method_exist(class_name, field_name, is_field=True)
        if should_exist and not is_field_name_exist:
            self.__console.print(f"\n[bold red]Field [bold white]'{field_name}'[/bold white] does not exist in class [bold white]'{class_name}'[/bold white]![/bold red]")
            return False
        # When field name should not exist but it does
        elif not should_exist and is_field_name_exist:
            self.__console.print(f"\n[bold red]Field [bold white]'{field_name}'[/bold white] has already existed in class [bold white]'{class_name}'[/bold white]![/bold red]")
            return False
        return True
    
    # Validate method name based on whether it should exist or not #
    def __validate_method_existence(self, class_name: str,  method_name: str, should_exist: bool) -> bool:
        # When method name should exist but it does not
        is_method_name_exist = self.__field_or_method_exist(class_name, method_name, is_field=False)
        if should_exist and not is_method_name_exist:
            self.__console.print(f"\n[bold red]Method [bold white]'{method_name}'[/bold white] does not exist in class [bold white]'{class_name}'[/bold white]![/bold red]")
            return False
        # When method name should not exist but it does
        elif not should_exist and is_method_name_exist:
            self.__console.print(f"\n[bold red]Method [bold white]'{method_name}'[/bold white] has already existed in class [bold white]'{class_name}'[/bold white]![/bold red]")
            return False
        return True
    
    # Check if we are able to rename field/method #
    def __check_field_or_method_rename(self, class_name: str, current_name: str, new_name: str, is_field: bool) -> bool:
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        if not is_class_exist:
            return
        if is_field:
            # Check if current field name exists or not
            is_current_field_name_exist = self.__validate_field_existence(class_name, current_name, should_exist=True)
             # If the field does not exist, stop
            if not is_current_field_name_exist:
                return False
             # Check if new field name exists or not
            is_new_name_exist = self.__validate_field_existence(class_name, new_name, should_exist=False)
            # If the field has already existed, stop
            if not is_new_name_exist:
                return False
        else:
            # Check if current method name exists or not
            is_current_method_name_exist = self.__validate_method_existence(class_name, current_name, should_exist=True)
             # If the method does not exist, stop
            if not is_current_method_name_exist:
                return False
             # Check if new method name exists or not
            is_new_name_exist = self.__validate_method_existence(class_name, new_name, should_exist=False)
            # If the method has already existed, stop
            if not is_new_name_exist:
                return False
        return True
    
    # Get the chosen field #
    def __get_chosen_field_or_method(self, class_name: str,  input_name: str, is_field: bool) -> Field | Method | None:
        # Get class object
        class_object = self.__class_list[class_name]
        # Select the correct list based on is_field
        if is_field:
            general_list = class_object._get_class_field_list()
        else:
            general_list = class_object._get_class_method_list()
        # Find the chosen object
        # Loop through the list to find the object name 
        for element in general_list:
            current_name = element._get_name()
            # If exists, return the field
            if current_name == input_name:
                return element
        return None
    
    ## PARAMETER RELATED ##
    
    # Parameter check #
    def __parameter_exist(self,class_name:str, method_name: str, parameter_name: str) -> bool:
        # Get method and parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        if method_name not in method_and_parameter_list:
           self.__console.print(f"\n[bold red]Method [bold white]'{method_name}'[/bold white] does not exist![/bold red]")
           return False
        parameter_list = method_and_parameter_list[method_name]
        for parameter in parameter_list:
            if parameter_name == parameter._get_parameter_name():
                return True
        return False
    
    # Validate parameter existence #
    def __validate_parameter_existence(self, class_name: str, method_name: str, parameter_name: str, should_exist: bool) -> bool:
        is_parameter_exist = self.__parameter_exist(class_name, method_name, parameter_name)
        # If should exist but not exist, return false
        if should_exist and not is_parameter_exist:
            self.__console.print(f"\n[bold red]Parameter [bold white]'{parameter_name}'[/bold white] does not exist![/bold red]")
            return False
        # If should not exist but exists, return false
        elif not should_exist and is_parameter_exist:
            self.__console.print(f"\n[bold red]Parameter [bold white]'{parameter_name}'[/bold white] has already existed![/bold red]")
            return False
        return True
    
    # Get chosen parameter #
    def __get_chosen_parameter(self, class_name: str, method_name: str, parameter_name: str) -> Parameter:
        # Get method and parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        parameter_list = method_and_parameter_list[method_name]
        for each_parameter in parameter_list:
            if each_parameter._get_parameter_name() == parameter_name:
                return each_parameter
        return None
           
    ## RELATIONSHIP RELATED ##
    
    # Relationship type check #
    def __type_exist(self, type_name: str) -> bool:
        RelationshipType = self.__user_view._get_enum_list()
        if type_name in RelationshipType._value2member_map_:
            return True
        return False
    
    # Validate type name based on whether it should exist or not #
    def __validate_type_existence(self, type_name: str, should_exist: bool) -> bool:
        is_type_exist = self.__type_exist(type_name)
        if should_exist and not is_type_exist:
            self.__console.print(f"\n[bold red]Type [bold white]'{type_name}'[/bold white] does not exist![/bold red]")
            return False
        return True

    # Check relationship exists or not #
    def __relationship_exist(self, source_class_name: str, destination_class_name: str) -> bool:
        # Get relationship list
        relationship_list = self.__relationship_list
        for each_relationship in relationship_list:
            current_source_class_name = each_relationship._get_source_class()
            current_destination_class_name = each_relationship._get_destination_class()
            if current_source_class_name == source_class_name and current_destination_class_name == destination_class_name:
                return True
        return False
    
    # Get chosen relationship #
    def __get_chosen_relationship(self, source_class_name: str, destination_class_name: str) -> Relationship:
        # Get relationship list
        relationship_list = self.__relationship_list
        for each_relationship in relationship_list:
            current_source_class_name = each_relationship._get_source_class()
            current_destination_class_name = each_relationship._get_destination_class()
            if current_source_class_name == source_class_name and current_destination_class_name == destination_class_name:
                return each_relationship
        return None
    
    # Get chosen relationship type #
    def __get_chosen_relationship_type(self, source_class_name: str, destination_class_name: str) -> str | None:
        current_relationship = self.__get_chosen_relationship(source_class_name, destination_class_name)
        if current_relationship is not None:
            return current_relationship._get_type()
        self.__console.print(f"\n[bold red]No relationship between class [bold white]'{source_class_name}'[/bold white] and class [bold white]'{destination_class_name}'[/bold white![/bold red]")
        return None
            
    #################################################################
    ### JSON FORMAT ###
    
    # Get field format list #
    def _get_field_format_list(self, class_object: Class) -> List[Dict]:
        # Get field list
        field_list = class_object._get_class_field_list()
         # Field format list
        field_list_format: List[Dict] = []
        for each_field in field_list:
            attr_json_format = each_field._convert_to_json_field()
            field_list_format.append(attr_json_format)
        return field_list_format
    
    # Get method format list #
    def _get_method_format_list(self, class_object: Class) -> List[Dict]:
        # Get field list
        method_list = class_object._get_class_method_list()
        # Field format list
        method_list_format: List[Dict] = []
        # Get method and parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_object._get_class_name())
        for each_method in method_list:
            method_json_format = each_method._convert_to_json_method()
            # Get current parameter list of current method
            parameter_list = method_and_parameter_list[each_method._get_name()]
            # Convert parameters to json format and save to a list
            parameter_format_list: List[Dict] = []
            for each_parameter in parameter_list:
                parameter_format_list.append(each_parameter._convert_to_json_parameter())
            # Add method format to the format list
            method_list_format.append(method_json_format)
            # Add parameter list to parameter format list
            for each_method_format in method_list_format:
                if each_method_format["name"] == each_method._get_name():
                    for each_param_format in parameter_format_list:    
                        each_method_format["params"].append(each_param_format)
        return method_list_format
    
    # Get relationship format list #
    def _get_relationship_format_list(self) -> List[Dict]:
        # Get relationship list
        relationship_list = self.__relationship_list
        # Relationship format list
        relationship_list_format: list[Dict] = []
        for each_relationship in relationship_list:
            rel_json_format = each_relationship._convert_to_json_relationship()
            relationship_list_format.append(rel_json_format)
        return relationship_list_format
    
    # Combine class json format #
    def _class_json_format(self, class_name: str) -> Dict:
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get class format
        class_format = class_object._convert_to_json_uml_class()
        # Assign class name
        class_format["name"] = class_object._get_class_name()
        # Field list format
        field_list_format: List[Dict] = self._get_field_format_list(class_object)       
        # Assign field list format
        class_format["fields"] = field_list_format
        # Method list format
        method_list_format: List[Dict] = self._get_method_format_list(class_object)
        # Assign method list format
        class_format["methods"] = method_list_format
        return class_format
    
    #################################################################
    ### SAVE/LOAD ###
    
    # Save data #
    def _save(self):
        # Prompt the user for a file name to save
        self.__console.print("\n[bold yellow]Please provide a name for the file you'd like to save or choose file from the list to override.[/bold yellow]")
        self.__console.print("[bold yellow]Type [bold white]'quit'[/bold white] to go back to main menu:[bold yellow]")
        # Show the list of saved files
        saved_list = self.__storage_manager._get_saved_list()
        self.__user_view._display_saved_list(saved_list)
        self.__console.print("[bold yellow]==>[/bold yellow] ", end="")
        user_input = input()
        # Prevent user from overriding NAME_LIST.json
        if user_input == "NAME_LIST":
            self.__console.print(f"\n[bold red]You can't save to [bold white]'{user_input}.json'[/bold white][bold red]")
            return 
        if user_input == "quit":
            self.__console.print("\n[bold green]Canceled saving![/bold green]")
            return
        # Class data list to put in the main data
        class_data_list = []
        # Relationship list to put in the main data
        relationship_data_list = []
        main_data = self.__update_main_data_from_loaded_file(user_input, class_data_list, relationship_data_list)
        self.__storage_manager._save_data_to_json(user_input, main_data)
        self.__console.print(f"\n[bold green]Successfully saved data to [bold white]'{user_input}.json'![/bold white][/bold green]")
        
    # Save for GUI #     
    def _save_gui(self, file_name, file_path):
        # Class data list to put in the main data
        class_data_list = []
        # Relationship list to put in the main data
        relationship_data_list = []
        main_data = self.__update_main_data_from_loaded_file(file_name, class_data_list, relationship_data_list)
        self.__storage_manager._save_data_to_json_gui(file_name, file_path, main_data)
    
    # Load data #
    def _load(self):
        # Prompt the user for a file name to save
        self.__console.print("\n[bold yellow]Please provide a name for the file you'd like to load.[/bold yellow]")
        self.__console.print("[bold yellow]Type [bold white]'quit'[/bold white] to go back to main menu:[/bold yellow]")
        # Show the list of saved files
        save_list = self.__storage_manager._get_saved_list()
        self.__user_view._display_saved_list(save_list)
        self.__console.print("[bold yellow]==>[/bold yellow] ", end="")
        user_input = input()
        # Prevent user from loading NAME_LIST.json
        if user_input == "NAME_LIST":
            self.__console.print(f"\n[bold red]You can't load from [bold white]'{user_input}.json'[/bold white][/bold red]")
            return 
        if user_input == "quit":
            self.__console.print("\n[bold green]Canceled loading![/bold green]")
            return
        is_loading = self._saved_file_name_check(user_input)
        if not is_loading:
            self.__console.print(f"\n[bold red]File [bold white]'{user_input}.json'[/bold white] does not exist[/bold red]")
            return
        main_data = self.__main_data = self.__storage_manager._load_data_from_json(user_input)
        self.__update_data_members(main_data)
        self.__check_file_and_set_status(user_input)
        self.__console.print(f"\n[bold green]Successfully loaded data from [bold white]'{user_input}.json'[/bold white]![/bold green]")
        
    # Update main data to store data to json file #
    def __update_main_data_from_loaded_file(self, user_input: str, class_data_list: List, relationship_data_list: List) -> Dict:
        relationship_data_list = self._get_relationship_format_list()
        main_data = self.__main_data
        # Add file name to saved list if it is a new one
        self.__storage_manager._add_name_to_saved_file(user_input)
        for class_name in self.__class_list:
            class_data_format = self._class_json_format(class_name)
            class_data_list.append(class_data_format)
        main_data["classes"] = class_data_list
        main_data["relationships"] = relationship_data_list
        return main_data
    
    # Update UMLCoreManager data after loading a file #
    def __update_data_members(self, main_data: Dict):
        class_data = main_data["classes"]
        relationship_data = main_data["relationships"]
        self.__reset_storage()
        # Set main data again
        self.__main_data = main_data
        # Re-create class, field, method and parameter
        extracted_class_data = self._extract_class_data(class_data)
        for each_pair in extracted_class_data:
            for class_name, data in each_pair.items(): 
                field_list = data['fields']
                method_param_list = data['methods_params']
                # Add the class
                self._add_class(class_name, is_loading=True)
                # Add the fields for the class
                for each_field in field_list:
                    self._add_field(class_name, each_field, is_loading=True)
                # Add the methods and its parameters for the class
                for method_name, param_list in method_param_list.items():
                    self._add_method(class_name, method_name, is_loading=True)
                    for param_name in param_list:
                        self._add_parameter(class_name, method_name, param_name, is_loading=True)
        # Re-create relationship 
        for each_dictionary in relationship_data:
            self._add_relationship(each_dictionary["source"], each_dictionary["destination"], each_dictionary["type"], is_loading=True)
        
    # This function help extracting class, field and method from json file and put into a list #
    def _extract_class_data(self, class_data: List[Dict]) -> List[Dict[str, Dict[str, List | Dict]]]:
        # Create a list of type List[Dict[str, Dict[str, List | Dict]]] (*NOTE* THIS TYPE CAUSED ME SEVERE HEADACHE T_T)
        class_info_list: List[Dict[str, Dict[str, List | Dict]]] = []
        # Loop through each class element
        for class_element in class_data:
            # Create a dictionary to store method name and its list of parameters
            method_and_param_list = {}
            # Get class name
            class_name = class_element["name"]
            # Get list of field names
            fields = [field["name"] for field in class_element["fields"]]
            # Extract method and its parameters into 'method_and_param_list'
            for method_element in class_element["methods"]:
                temp_param_list: List[str] = []
                for param_element in method_element["params"]:
                    temp_param_list.append(param_element["name"])
                method_and_param_list[method_element["name"]] = temp_param_list
            class_info_list.append({class_name: {'fields': fields, 'methods_params': method_and_param_list}})
        return class_info_list
    
    # Delete Saved File #
    def _delete_saved_file(self):
        self.__console.print("\n[bold yellow]Please choose a file you want to delete.[/bold yellow]")
        self.__console.print("[bold yellow]Type [bold white]'quit'[/bold white] to go back to main menu:[/bold yellow]")
        saved_list = self.__storage_manager._get_saved_list()
        self.__user_view._display_saved_list(saved_list)
        user_input = input()
        # Prevent user from loading NAME_LIST.json
        if user_input == "NAME_LIST":
            self.__console.print(f"\n[bold red]You can't delete file [bold white]'{user_input}.json'[/bold white][/bold red]")
            return 
        if user_input == "quit":
            self.__console.print("\n[bold green]Canceled loading![/bold green]")
            return
        is_file_exist = self._check_saved_file_exist(user_input)
        if not is_file_exist:
            self.__console.print(f"[bold red]File [bold white]'{user_input}.json'[/bold white] does not exist![/bold red]")
            return
        # Get saved file's name list
        save_list = self.__storage_manager._get_saved_list()
        for dictionary in save_list:
            if user_input in dictionary:
                save_list.remove(dictionary)
        # Update the saved list 
        self.__storage_manager._update_saved_list(save_list)
        # Physically remove the file   
        file_path = f"UML_UTILITY/SAVED_FILES/{user_input}.json"
        os.remove(file_path)
        self.__console.print(f"\n[bold green]Successfully removed file [bold white]'{user_input}.json'[/bold white][/bold green]")
        
    # Check if a saved file exist #
    def _check_saved_file_exist(self, file_name: str):
        saved_list = self.__storage_manager._get_saved_list()
        for element in saved_list:
            for name in element:
                if file_name == name:
                    return True
        return False
    
    # End Session To Go Back To Blank Program #
    def _end_session(self):
        self.__set_all_file_off()
        self.__reset_storage()
        self.__console.print("\n[bold green]Successfully back to default program![/bold green]")
    
    # Get active file #
    def _get_active_file(self) -> str:
        saved_list = self.__storage_manager._get_saved_list()
        for each_dictionary in saved_list:
            for key, val in each_dictionary.items():
                if val == "on":
                    return key
        return "No active file!"
    
    # Clear the current active file #
    def _clear_current_active_data(self):
        saved_list = self.__storage_manager._get_saved_list()
        if len(saved_list) == 0:
            self.__console.print("\n[bold red]No active file to clear data![bold red]")
            return
        current_active_file = self._get_active_file()
        if current_active_file == "No active file!":
            self.__console.print("\n[bold red]No active file![bold red]")
            return
        self.__reset_storage()
        self.__storage_manager._save_data_to_json(current_active_file, self.__main_data)
        self.__console.print(f"\n[bold green]Successfully clear data in file [bold white]'{current_active_file}.json'[/bold white][/bold green]")
        
    def _exit(self):
        self.__set_all_file_off()
        self.__console.print("\n[bold green]Exited Program[/bold green]")
    
    # Set all file status to off #
    def __set_all_file_off(self):
        saved_list = self.__storage_manager._get_saved_list()
        for each_dictionary in saved_list:
            for key in each_dictionary:
                each_dictionary[key] = "off"
        self.__storage_manager._update_saved_list(saved_list)
    
    # Set file status #
    def __set_file_status(self, file_name: str, status: str):
        saved_list = self.__storage_manager._get_saved_list()
        for each_dictionary in saved_list:
            for key in each_dictionary:
                if key == file_name:
                    each_dictionary[key] = status
    
    # Check file name and set its status #               
    def __check_file_and_set_status(self, file_name: str) -> str:
        saved_list = self.__storage_manager._get_saved_list()
        for each_dictionary in saved_list:
            for key in each_dictionary:
                if each_dictionary[key] == "on":
                    each_dictionary[key] = "off"
        self.__set_file_status(file_name, status="on")
        # Update the saved list 
        self.__storage_manager._update_saved_list(saved_list)
        
    # Reset all storage #
    def __reset_storage(self):
        self.__class_list: Dict[str, Class] = {}
        self.__relationship_list: List = []
        self.__main_data: Dict = {}
    
    #################################################################
    ### UTILITY FUNCTIONS ###  
        
    # Saved file check #
    def _saved_file_name_check(self, save_file_name: str) -> bool:
        saved_list = self.__storage_manager._get_saved_list()
        for each_pair in saved_list:
            for file_name in each_pair:
                if file_name == save_file_name:
                    return True
        return False
                
    # Update main data wrapper #
    def _update_main_data_for_every_action(self):
        # Class data list to put in the main data
        class_data_list = []
        relationship_data_list = self._get_relationship_format_list()
        main_data = self.__main_data
        # Add file name to saved list if it is a new one
        for class_name in self.__class_list:
            class_data_format = self._class_json_format(class_name)
            class_data_list.append(class_data_format)
        main_data["classes"] = class_data_list
        main_data["relationships"] = relationship_data_list
    
    # Validate entities (Class, Method, Field, Parameter)          
    def _validate_entities(
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
        """
        General validation function for class, field, method, and parameter existence.
        - class_name: Name of the class to check.
        - field_name: Name of the field to check.
        - method_name: Name of the method to check.
        - parameter_name: Name of the parameter to check.
        - class_should_exist: Whether the class should exist (True) or not (False).
        - field_should_exist: Whether the field should exist (True) or not (False).
        - method_should_exist: Whether the method should exist (True) or not (False).
        - parameter_should_exist: Whether the parameter should exist (True) or not (False).
    
        Returns True if all required entities exist (or don't exist) as expected, otherwise False.
        """
        # Check class existence if specified
        if class_name is not None and class_should_exist is not None:
            is_class_exist = self.__validate_class_existence(class_name, class_should_exist)
            if not is_class_exist:
                return False
        # Check field existence if specified
        if field_name is not None and field_should_exist is not None:
            is_field_exist = self.__validate_field_existence(class_name, field_name, field_should_exist)
            if not is_field_exist:
                return False
        # Check method existence if specified
        if method_name is not None and method_should_exist is not None:
            is_method_exist = self.__validate_method_existence(class_name, method_name, method_should_exist)
            if not is_method_exist:
                return False
        # Check parameter existence if specified
        if parameter_name is not None and parameter_should_exist is not None:
            is_parameter_exist = self.__validate_parameter_existence(class_name, method_name, parameter_name, parameter_should_exist)
            if not is_parameter_exist:
                return False
        # All checks passed
        return True
    
    # Sorting Class List #
    def _sort_class_list(self):
        class_list = self.__class_list
        if len(class_list) == 0:
            self.__console.print("\n[bold red]No class to sort![/bold red]")
            return
        self.__class_list = dict(sorted(self.__class_list.items()))
        self._update_main_data_for_every_action()
        self.__user_view._display_uml_data(self.__main_data)
                       
###################################################################################################