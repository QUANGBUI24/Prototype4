class UMLAttribute:
    # UML class attribute constructor
    # Create an attribute to add to the UML Class
    def __init__(
        self,
        attribute_name: str,
    ):
        self.__attribute_name = attribute_name

    def __str__(self):
            return f"{self.__attribute_name}"
        
    #################################################################
    # Method to get attribute's data members #
    def _get_attribute_name(self) -> str:
        return self.__attribute_name

    #################################################################
    # Method to modify attribute's data members #
    def _set_attribute_name(self, new_name: str):
        self.__attribute_name = new_name

    #################################################################
    # Method to convert attribute to json format
    def _convert_to_json_attribute(self) -> dict[str, str]:
        return {"name": self.__attribute_name}