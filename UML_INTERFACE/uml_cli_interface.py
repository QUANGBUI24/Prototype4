from enum import Enum

class InterfaceOptions(Enum):
    WORK = "work"
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


class UMLClassInterfaceOption(Enum):
    ADD_CLASS = "add_class"
    DELETE_CLASS = "delete_class"
    RENAME = "rename_class"
    ADD_ATTR = "add_attr"
    DELETE_ATTR = "delete_attr"
    RENAME_ATTR = "rename_attr"
    ADD_REL = "add_rel"
    DELETE_REL = "delete_rel"
    HELP = "help"
    BACK = "back"


def prompt_main_menu():
    print("Welcome To Our UML Program!")
    print("Type 'work' start working with class(es)")
    print("Type 'list_class' to see the list of all created class(es)")
    print("Type 'class_detail <class_name>' to see the detail of the chosen class")
    print("Type 'class_rel' to see the relationships between class(es)")
    print("Type 'saved_list' to see the list of saved files")
    print("Type 'save' to save data")
    print("Type 'load' to load data from saved files")
    print("Type 'delete_saved' to delete saved file")
    print("Type 'clear_data' to delete all the data in the current storage")
    print("Type 'default' to go back to blank program")
    print("Type 'sort' to sort the class list in alphabetical order")
    print("Type 'help' to see the instructions")
    print("Type 'exit' to quit program")


def prompt_working_menu():
    # Class
    print("Type 'add_class <class_name>' to add a class")
    print("Type 'delete_class <class_name>' to delete a class")
    print("Type 'rename_class <class_name> <new_name>' to rename a class")
    # Attribute
    print("Type 'add_attr <class_name> <attr_name>' to add an attribute")
    print(
        "Type 'delete_attr <class_name> <attr_name>' to delete an attribute from the chosen class"
    )
    print(
        "Type 'rename_attr <class_name> <current_attribute_name> <new_name>' to rename an attribute"
    )
    # Relationship
    print(
        "Type 'add_rel <source_class> <destination_class_name> <relationship_level>' to add relationship and relationship level"
    )
    print(
        "Type 'delete_rel <chosen_class_name> <destination_class_name>' to delete a relationship"
    )
    print("Type 'help' to see the instruction")
    print("Type 'back' to go back to main menu'")