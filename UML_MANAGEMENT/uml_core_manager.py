###################################################################################################

from enum import Enum
from typing import Dict, List
from UML_CORE.UML_CLASS.uml_class import UMLClass as Class
from UML_CORE.UML_ATTRIBUTE.uml_attribute import UMLAttribute as Attribute
from UML_CORE.UML_METHOD.uml_method import UMLMethod as Method
from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship as Relationship
from UML_CORE.UML_PARAMETER.uml_parameter import UMLParameter as Parameter

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
        chosen_attribute = self.__get_chosen_attribute(class_name, attribute_name)
        # Remove the chosen attribute 
        attribute_list.remove(chosen_attribute)
        print(f"\nSuccessfully removed attribute '{attribute_name}'!")
        
    # Rename attribute #
    def _rename_attribute(self, class_name: str, current_attribute_name: str, new_attribute_name: str):
        is_able_to_rename = self.__check_attribute_rename(class_name, current_attribute_name, new_attribute_name)
        if not is_able_to_rename:
            return
        # Get the attribute
        chosen_attribute = self.__get_chosen_attribute(class_name, current_attribute_name)
        chosen_attribute._set_attribute_name(new_attribute_name)
        print(f"\nSuccessfully renamed from attribute '{current_attribute_name}' to attribute '{new_attribute_name}'!")
        
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
        is_relationship_exist = self.__relationship_exist(source_class_name)
        if is_relationship_exist:
            print(f"\nRelation ship between class '{source_class_name}' to class '{destination_class_name}' has already existed!")
            return
        # Checking type
        is_type_exist = self.__validate_type_existence(rel_type, should_exist=True)
        if not is_type_exist:
            return
        # Get class object
        source_class_object = self.__class_list[source_class_name]
        # Get relationship list
        source_class_relationship_list = source_class_object._get_class_relationship_list()
        # Create new relationship
        new_relationship = self.create_relationship(source_class_name, destination_class_name, rel_type)
        # Add new relationship to the list
        source_class_relationship_list.append(new_relationship)
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
        is_relationship_exist = self.__relationship_exist(source_class_name)
        if not is_relationship_exist:
            print(f"\nRelation ship between class '{source_class_name}' to class '{destination_class_name}' does not exist!")
            return
        # Get class object
        source_class_object = self.__class_list[source_class_name]
        # Get relationship list
        source_class_relationship_list = source_class_object._get_class_relationship_list()
        # Get chosen relationship
        current_relationship = self.__get_chosen_relationship(source_class_name)
        # Remove relationship
        source_class_relationship_list.remove(current_relationship)
        print(f"\nSuccessfully removed relationship between class '{source_class_name}' to class '{destination_class_name}'")
        
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
        # Get class object
        class_object = self.__class_list[new_name]
        # Get relationship list
        relationship_list = class_object._get_class_relationship_list()
        # Loop through the relationship list
        for each_relationship in relationship_list:
            source_name = each_relationship._get_source_class()
            destination_name = each_relationship._get_destination_class()
            if source_name == current_name:
                each_relationship._set_source_class(new_name)
            elif destination_name == current_name:
                each_relationship._set_destination_class(new_name)
    
    ## ATTRIBUTE RELATED ##
    
    # Check attribute name exist or not #
    def __attribute_exist(self, class_name: str, attribute_name: str, ) -> bool:
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get attribute list
        attribute_list = class_object._get_class_attribute_list()
        # Loop through the list to find the attribute name 
        for each_attribute in attribute_list:
            current_attribute_name = each_attribute._get_attribute_name()
            # If exists, return true
            if current_attribute_name == attribute_name:
                return True
        return False
    
    # Validate attribute name based on whether it should exist or not #
    def __validate_attribute_existence(self, class_name: str,  attribute_name: str, should_exist: bool) -> bool:
        # When attribute name should exist but it does not
        is_attribute_name_exist = self.__attribute_exist(class_name, attribute_name)
        if should_exist and not is_attribute_name_exist:
            print(f"\nAttribute '{attribute_name}' does not exist in class '{class_name}'!")
            return False
        # When attribute name should not exist but it does
        elif not should_exist and is_attribute_name_exist:
            print(f"\nAttribute '{attribute_name}' has already existed in class '{class_name}'!")
            return False
        return True
    
    # Check if we are able to rename attribute #
    def __check_attribute_rename(self, class_name: str, current_attribute_name: str, new_attribute_name: str) -> bool:
        # Check if current attribute name exists or not
        is_current_attribute_name_exist = self.__validate_attribute_existence(class_name, current_attribute_name, should_exist=True)
        # If the attribute does not exist, stop
        if not is_current_attribute_name_exist:
            return False
        # Check if new attribute name exists or not
        is_new_attribute_name_exist = self.__validate_attribute_existence(class_name, new_attribute_name, should_exist=False)
        # If the attribute has already existed, stop
        if not is_new_attribute_name_exist:
            return False
        return True
    
    # Get the chosen attribute #
    def __get_chosen_attribute(self, class_name: str,  attribute_name: str) -> Attribute | None:
        # Get class object
        class_object = self.__class_list[class_name]
        # Get attribute list
        attribute_list = class_object._get_class_attribute_list()
        # Find the chosen attribute:
        # Loop through the list to find the attribute name 
        for each_attribute in attribute_list:
            current_attribute_name = each_attribute._get_attribute_name()
            # If exists, return the attribute
            if current_attribute_name == attribute_name:
                return each_attribute
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
    def __relationship_exist(self, source_class_name: str) -> bool:
        # Get class object
        source_class_object = self.__class_list[source_class_name]
        # Get relationship list
        source_class_relationship_list = source_class_object._get_class_relationship_list()
        for each_relationship in source_class_relationship_list:
            current_source_class_name = each_relationship._get_source_class()
            if current_source_class_name == source_class_name:
                return True
        return False
    
    # Get chosen relationship #
    def __get_chosen_relationship(self, source_class_name: str):
        # Get class object
        class_object = self.__class_list[source_class_name]
        # Get relationship list
        relationship_list = class_object._get_class_relationship_list()
        for each_relationship in relationship_list:
            current_source_class_name = each_relationship._get_source_class()
            if current_source_class_name == source_class_name:
                return each_relationship
        return None
                       
    #################################################################
    ### UTILITY FUNCTIONS ###  
    
    # Display type Enum #
    def __display_type_enum(self):
        print("|=================|")
        for type in RelationshipType:
            print(f"{type.value:^20}")
        print("|=================|")
    
    # Display info #
    def _display_attr(self):
        for key, val in self.__class_list.items():
            attr_list = val._get_class_attribute_list()
            for attr in attr_list:
                print(attr)
                
    def _display_rel(self):
        for key, val in self.__class_list.items():
            rel_list = val._get_class_relationship_list()
            for rel in rel_list:
                print(rel)
                
    # Combine json format #
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
        # Get attribute list
        attribute_list = class_object._get_class_attribute_list()
        # Field list
        field_list_format: List[Dict]= []
        for each_attribute in attribute_list:
            attr_json_format = each_attribute._convert_to_json_attribute()
            field_list_format.append(attr_json_format)
        # Assign field list
        class_format["fields"] = field_list_format
        return class_format
    
    def _final_format(self, class_format: Dict):
        final_format = {"classes":[], "relationship":[]}
        final_format["classes"].append(class_format)
        return final_format
                
###################################################################################################