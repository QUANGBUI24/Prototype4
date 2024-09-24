from typing import Dict, List

from UML_CORE.UML_ATTRIBUTE.uml_attribute import UMLAttribute as Attribute
from UML_CORE.UML_METHOD.uml_method import UMLMethod as Method
from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship as Relationship


class UMLClass:
    #################################################################
    # Uml class constructor
    # Create UML class with a name including:
    def __init__(self, class_name: str):
        self.__class_name = class_name
        # Store attribute name and the related attribute object
        # so we can easily access to the its details
        self.__attribute_list: List[Attribute] = []
        # Store method name and the related method object
        # so we can easily access to the its details
        self.__method_list: List[Method] = []
        # Store source class, destination class, and the type of relationship (e.g. Composition, Aggregation, etc.)
        self.__relationship_list: List[Relationship] = []

    #################################################################
    # Method to get UML class's data members #
    def _get_class_name(self) -> str:
        return self.__class_name

    def _get_class_attribute_list(self) -> List[Attribute]:
        return self.__attribute_list

    def _get_class_method_list(self) -> List[Method]:
        return self.__method_list

    def _get_class_relationship_list(self) -> List[Relationship]:
        return self.__relationship_list

    #################################################################
    # Method to modify UML class's data members #
    def _set_class_name(self, new_class_name: str):
        self.class_name = new_class_name

    def _set_class_attribute_list(self, new_attribute_list: List[Attribute]):
        self.__attribute_list = new_attribute_list

    def _set_class_method_list(self, new_method_list: List[Method]):
        self.__method_list = new_method_list

    def _set_class_relationship_list(
        self, new_relationship_list: List[Relationship]
    ):
        self.__relationship_list = new_relationship_list
        
    #################################################################
    # Method to convert uml class to json format #
    def _convert_to_json_uml_class(self) -> dict[str, list]:
        return {
            "name":self.__class_name,
            "fields":[],
            "methods":[]
        }
    