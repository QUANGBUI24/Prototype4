###################################################################################################

from enum import Enum
from typing import Dict, List
from UML_CORE.UML_CLASS.uml_class import UMLClass as Class
from UML_CORE.UML_ATTRIBUTE.uml_attribute import UMLAttribute as Attribute
from UML_CORE.UML_METHOD.uml_method import UMLMethod as Method
from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship as Relationship
from UML_CORE.UML_PARAMETER.uml_parameter import UMLParameter as Parameter
from UML_MANAGER.uml_storage_manager import UMLStorageManager as Storage

###################################################################################################
### ENUM FOR RELATIONSHIP TYPE ###

class RelationshipType(Enum):
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"
    INHERITANCE = "inheritance"
    REALIZATION = "realization"
    
###################################################################################################

class UMLCoreManager:
    
    #################################################################
    
    # UML Class Manager Constructor #
    def __init__(self):
        # {class_name : Class} pair
        self.__class_list: Dict[str, Class] = {}
        self.__storage: Storage = Storage()
        self.__relationship_list: List = []
        self.__main_data: Dict = {{"classes":[]}, {"relationships":[]}}
        
    def _get_class_list(self) -> Dict[str, Class]:
        return self.__class_list
        
    #################################################################
    ### STATIC FUNCTIONS ###

    # Class creation method #
    @staticmethod
    def create_class(class_name: str) -> Class:
        return Class(class_name)
    
    # Attribute creation method #
    @staticmethod
    def create_attribute(attribute_name: str) -> Attribute:
        return Attribute(attribute_name)
    
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
    def _add_class(self, class_name: str):
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=False)
        # If the class has already existed, stop
        if not is_class_exist:
            return
        # Else, add the class
        new_class = self.create_class(class_name)
        self.__class_list[class_name] = new_class
        print(f"\nSuccessfully added class '{class_name}'!")
        
    # Delete class #
    def _delete_class(self, class_name: str):
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Else, delete class
        self.__class_list.pop(class_name)
        print(f"\nSuccessfully removed class '{class_name}'!")
        
    # Rename class #
    def _rename_class(self, current_name: str, new_name: str):
        # Check if we are able to rename
        is_able_to_rename = self.__check_class_rename(current_name, new_name)
        # If not, stop
        if not is_able_to_rename:
            return
        # Update the key
        self.__class_list[new_name] = self.__class_list.pop(current_name)
        # Update the real class
        class_object = self.__class_list[new_name]
        class_object._set_class_name(new_name)   
        # Update name in relationship list
        self.__update_name_in_relationship(current_name, new_name)
        print(f"\nSuccessfully renamed from class '{current_name}' to class '{new_name}'!")
        
    ## ATTRIBUTE RELATED ##
    
    # Add attribute #
    def _add_attribute(self, class_name: str, attribute_name: str):
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Check if attribute exists or not
        is_attribute_exist = self.__validate_attribute_existence(class_name, attribute_name, should_exist=False)
        # If the attribute has already existed, stop
        if not is_attribute_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get attribute list
        attribute_list = class_object._get_class_attribute_list()
        # Create new attribute
        new_attribute = self.create_attribute(attribute_name)
        # Add attribute
        attribute_list.append(new_attribute)
        print(f"\nSuccessfully added attribute '{attribute_name}'!")
        
    # Delete attribute #
    def _delete_attribute(self, class_name: str, attribute_name: str):
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Check if attribute exists or not
        is_attribute_exist = self.__validate_attribute_existence(class_name, attribute_name, should_exist=True)
        # If the attribute does not exist, stop
        if not is_attribute_exist:
            return
         # Get class object
        class_object = self.__class_list[class_name]
        # Get attribute list
        attribute_list = class_object._get_class_attribute_list()
        # Get the attribute
        chosen_attribute = self.__get_chosen_attribute_or_method(class_name, attribute_name, is_attribute=True)
        # Remove the chosen attribute 
        attribute_list.remove(chosen_attribute)
        print(f"\nSuccessfully removed attribute '{attribute_name}'!")
        
    # Rename attribute #
    def _rename_attribute(self, class_name: str, current_attribute_name: str, new_attribute_name: str):
        is_able_to_rename = self.__check_attribute_or_method_rename(class_name, current_attribute_name, new_attribute_name, is_attribute=True)
        if not is_able_to_rename:
            return
        # Get the attribute
        chosen_attribute = self.__get_chosen_attribute_or_method(class_name, current_attribute_name, is_attribute=True)
        chosen_attribute._set_name(new_attribute_name)
        print(f"\nSuccessfully renamed from attribute '{current_attribute_name}' to attribute '{new_attribute_name}'!")
        
    ## METHOD RELATED ##
    
    # Add method #
    def _add_method(self, class_name: str, method_name: str):
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Check if method exists or not
        is_method_exist = self.__validate_method_existence(class_name, method_name, should_exist=False)
        # If the attribute has already existed, stop
        if not is_method_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get attribute list
        method_list = class_object._get_class_method_list()
        # Create new method
        new_method = self.create_method(method_name)
        # Add method
        method_list.append(new_method)
        print(f"\nSuccessfully added method '{method_name}'!")
        
    # Delete method #
    def _delete_method(self, class_name: str, method_name: str):
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Check if method exists or not
        is_method_exist = self.__validate_method_existence(class_name, method_name, should_exist=True)
        # If the method does not exist, stop
        if not is_method_exist:
            return
         # Get class object
        class_object = self.__class_list[class_name]
        # Get method list
        method_list = class_object._get_class_method_list()
        # Get the method
        chosen_method = self.__get_chosen_attribute_or_method(class_name, method_name, is_attribute=False)
        # Remove the chosen attribute 
        method_list.remove(chosen_method)
        print(f"\nSuccessfully removed method '{method_name}'!")
        
    # Rename method #
    def _rename_method(self, class_name: str, current_method_name: str, new_method_name: str):
        is_able_to_rename = self.__check_attribute_or_method_rename(class_name, current_method_name, new_method_name, is_attribute=False)
        if not is_able_to_rename:
            return
        # Get the method
        chosen_method = self.__get_chosen_attribute_or_method(class_name, current_method_name, is_attribute=False)
        chosen_method._set_name(new_method_name)
        print(f"\nSuccessfully renamed from method '{current_method_name}' to method '{new_method_name}'!")
        
    ## RELATIONSHIP RELATED ##
    
    # Add relationship #
    def _add_relationship(self, source_class_name: str, destination_class_name: str, rel_type: str):
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
            print(f"\nRelation ship between class '{source_class_name}' to class '{destination_class_name}' has already existed!")
            return
        # Checking type
        is_type_exist = self.__validate_type_existence(rel_type, should_exist=True)
        if not is_type_exist:
            return
        # Create new relationship
        new_relationship = self.create_relationship(source_class_name, destination_class_name, rel_type)
        # Add new relationship to the list
        self.__relationship_list.append(new_relationship)
        print(f"\nSuccessfully added relationship from class '{source_class_name}' to class '{destination_class_name}' of type '{rel_type}'!")
        
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
            print(f"\nRelation ship between class '{source_class_name}' to class '{destination_class_name}' does not exist!")
            return
        # Get chosen relationship
        current_relationship = self.__get_chosen_relationship(source_class_name)
        # Remove relationship
        self.__relationship_list.remove(current_relationship)
        print(f"\nSuccessfully removed relationship between class '{source_class_name}' to class '{destination_class_name}'!")      
        
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
            print(f"\nClass '{class_name}' does not exist!")
            return False
        # When class name should not exist but it does
        elif not should_exist and is_class_name_exist:
            print(f"\nClass '{class_name}' has already existed!")
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
    
    ## ATTRIBUTE AND METHOD RELATED ##
    
    # Check attribute name exist or not #
    def __attribute_or_method_exist(self, class_name: str, input_name: str, is_attribute: bool) -> bool:
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Select the correct list based on is_attribute
        if is_attribute:
            general_list = class_object._get_class_attribute_list()
        else:
            general_list = class_object._get_class_method_list()
        # Loop through the list to find the attribute name 
        for element in general_list:
            current_name = element._get_name()
            # If exists, return true
            if current_name == input_name:
                return True
        return False
    
    # Validate attribute name based on whether it should exist or not #
    def __validate_attribute_existence(self, class_name: str,  attribute_name: str, should_exist: bool) -> bool:
        # When attribute name should exist but it does not
        is_attribute_name_exist = self.__attribute_or_method_exist(class_name, attribute_name, is_attribute=True)
        if should_exist and not is_attribute_name_exist:
            print(f"\nAttribute '{attribute_name}' does not exist in class '{class_name}'!")
            return False
        # When attribute name should not exist but it does
        elif not should_exist and is_attribute_name_exist:
            print(f"\nAttribute '{attribute_name}' has already existed in class '{class_name}'!")
            return False
        return True
    
    # Validate method name based on whether it should exist or not #
    def __validate_method_existence(self, class_name: str,  method_name: str, should_exist: bool) -> bool:
        # When method name should exist but it does not
        is_method_name_exist = self.__attribute_or_method_exist(class_name, method_name, is_attribute=False)
        if should_exist and not is_method_name_exist:
            print(f"\nMethod '{method_name}' does not exist in class '{class_name}'!")
            return False
        # When method name should not exist but it does
        elif not should_exist and is_method_name_exist:
            print(f"\nMethod '{method_name}' has already existed in class '{class_name}'!")
            return False
        return True
    
    # Check if we are able to rename attribute #
    def __check_attribute_or_method_rename(self, class_name: str, current_name: str, new_name: str, is_attribute: bool) -> bool:
        if is_attribute:
            # Check if current attribute name exists or not
            is_current_attribute_name_exist = self.__validate_attribute_existence(class_name, current_name, should_exist=True)
             # If the attribute does not exist, stop
            if not is_current_attribute_name_exist:
                return False
             # Check if new attribute name exists or not
            is_new_name_exist = self.__validate_attribute_existence(class_name, new_name, should_exist=False)
            # If the attribute has already existed, stop
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
    
    # Get the chosen attribute #
    def __get_chosen_attribute_or_method(self, class_name: str,  input_name: str, is_attribute: bool) -> Attribute | Method | None:
        # Get class object
        class_object = self.__class_list[class_name]
        # Select the correct list based on is_attribute
        if is_attribute:
            general_list = class_object._get_class_attribute_list()
        else:
            general_list = class_object._get_class_method_list()
        # Find the chosen object
        # Loop through the list to find the object name 
        for element in general_list:
            current_name = element._get_name()
            # If exists, return the attribute
            if current_name == input_name:
                return element
        return None
            
    ## RELATIONSHIP RELATED ##
    
    # Relationship type check #
    def __type_exist(self, type_name: str) -> bool:
        for relationship_type in RelationshipType:
            if relationship_type.value == type_name:
                return True
        return False
    
    # Validate type name based on whether it should exist or not #
    def __validate_type_existence(self, type_name: str, should_exist: bool) -> bool:
        is_type_exist = self.__type_exist(type_name)
        if should_exist and not is_type_exist:
            print(f"\nType '{type_name}' does not exist!")
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
    def __get_chosen_relationship(self, source_class_name: str):
        # Get relationship list
        relationship_list = self.__relationship_list
        for each_relationship in relationship_list:
            current_source_class_name = each_relationship._get_source_class()
            if current_source_class_name == source_class_name:
                return each_relationship
        return None
    
    #################################################################
    ### JSON FORMAT ###
    
    # Get attribute format list #
    def _get_attribute_format_list(self, class_object: Class) -> List[Dict]:
        # Get attribute list
        attribute_list = class_object._get_class_attribute_list()
         # Field format list
        field_list_format: List[Dict] = []
        for each_attribute in attribute_list:
            attr_json_format = each_attribute._convert_to_json_attribute()
            field_list_format.append(attr_json_format)
        return field_list_format
    
    # Get method format list #
    def _get_method_format_list(self, class_object: Class) -> List[Dict]:
        # Get attribute list
        method_list = class_object._get_class_method_list()
         # Field format list
        method_list_format: List[Dict] = []
        for each_method in method_list:
            method_json_format = each_method._convert_to_json_method()
            method_list_format.append(method_json_format)
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
        field_list_format: List[Dict] = self._get_attribute_format_list(class_object)       
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
    def save(self):
        # Prompt the user for a file name to save
        print("\nPlease provide a name for the file you'd like to save or choose file from the list to override.")
        print("Type 'quit' to go back to main menu:")
        # Show the list of saved files
        self.__display_saved_file_name()
        print("==> ", end="")
        user_input = input()
        # Prevent user from overriding NAME_LIST.json
        if user_input == "NAME_LIST":
            print(f"\nYou can't save to '{user_input}.json'")
            return 
        if user_input == "quit":
            return
        class_data_list = []
        relationship_data_list = self._get_relationship_format_list()
        # Add file name to saved list if it is a new one
        self.__storage._add_name_to_saved_file(user_input)
        for class_name in self.__class_list:
            class_data_format = self._class_json_format(class_name)
            class_data_list.append(class_data_format)
            self.__storage._save_data_to_json(user_input, class_data_list, relationship_data_list)
        print(f"\nSuccessfully saved data to '{user_input}.json'!")
        
    # Load data #
    def load(self):
        # Prompt the user for a file name to save
        print("\nPlease provide a name for the file you'd like to save or choose file from the list to override.")
        print("Type 'quit' to go back to main menu:")
        # Show the list of saved files
        self.__display_saved_file_name()
        print("==> ", end="")
        user_input = input()
        # Prevent user from loading NAME_LIST.json
        if user_input == "NAME_LIST":
            print(f"\nYou can't load from '{user_input}.json'")
            return 
        if user_input == "quit":
            return
        is_loading = self.__saved_file_name_check(user_input)
        if not is_loading:
            print(f"\nFile '{user_input}.json' does not exist")
            return
        self.__main_data = self.__storage._load_data_from_json(user_input)
        
            
                       
    #################################################################
    ### UTILITY FUNCTIONS ###  
    
    # Display type Enum #
    def __display_type_enum(self):
        print("|=================|")
        for type in RelationshipType:
            print(f"{type.value:^20}")
        print("|=================|")
        
    # Display saved file's names #
    def __display_saved_file_name(self):
        saved_list = self.__storage._get_saved_list()
        if len(saved_list) == 0:
            print("\nNo saved file exists!")
            return
        print("\n|===================|")
        for dictionary in saved_list:
            for key in dictionary:
                print(f"{key:^20}")
        print("|===================|\n")
        
    # Saved file check #
    def __saved_file_name_check(self, save_file_name: str) -> bool:
        saved_list = self.__storage._get_saved_list()
        for each_pair in saved_list:
            for file_name in each_pair:
                if file_name == save_file_name:
                    return True
        return False
    
    # Display info (TEMPORARY) #
    def _display_attr(self):
        for key, val in self.__class_list.items():
            attr_list = val._get_class_attribute_list()
            for attr in attr_list:
                print(attr)
                
    def _display_method(self):
        for key, val in self.__class_list.items():
            method_list = val._get_class_method_list()
            for method in method_list:
                print(method)
                
    def _display_rel(self):
        rel_list = self.__relationship_list
        for rel in rel_list:
            print(rel)
            
                
###################################################################################################