
from UML_MANAGEMENT.uml_core_manager import UMLCoreManager as Manager
import json
import os

UML_MANAGER = Manager()


def save_data_to_json(file_name: str, format):
    file_path = f"UML_SAVE_FILES/{file_name}.json"
    # If the file doesn't exist, create it and write the data list
    with open(file_path, "w") as json_file:
        json.dump(format, json_file, indent=4)
        print("\nSuccessfully saved data!")
       

def main():
    UML_MANAGER._add_class("Human")
    UML_MANAGER._add_attribute("Human", "Body")
    UML_MANAGER._add_attribute("Human", "Head")
    UML_MANAGER._add_attribute("Human", "Legs")
    
    UML_MANAGER._add_class("House")
    UML_MANAGER._add_attribute("House", "Roof")
    UML_MANAGER._add_attribute("House", "Garage")
    UML_MANAGER._add_attribute("House", "Door")
    
    
    UML_MANAGER._add_class("Cat")
    UML_MANAGER._add_relationship("Human", "Cat", "aggregation")
    UML_MANAGER._delete_relationship("Human", "Cat")
    print()
    # UML_MANAGER._display_rel()
    test_format = UML_MANAGER._class_json_format("Human")
    final_format = UML_MANAGER._final_format(test_format)
    save_data_to_json("data", final_format)
    
    # test_format = UML_MANAGER._class_json_format("House")
    # final_format = UML_MANAGER._final_format(test_format)
    # save_data_to_json("data", final_format)
    
    # print(test_format)
  


if __name__ == "__main__":
    main()
