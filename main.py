
from UML_MANAGER.uml_core_manager import UMLCoreManager as Manager

UML_MANAGER = Manager()
class_list = UML_MANAGER._get_class_list()      

def main():
    UML_MANAGER._add_class("Human")
    UML_MANAGER._add_attribute("Human", "Body")
    UML_MANAGER._add_attribute("Human", "Head")
    UML_MANAGER._add_attribute("Human", "Legs")
    
    UML_MANAGER._add_method("Human", "Walk")
    UML_MANAGER._add_method("Human", "Run")

    # print()
    # UML_MANAGER._display_method()
    
    UML_MANAGER._add_class("House")
    UML_MANAGER._add_attribute("House", "Roof")
    UML_MANAGER._add_attribute("House", "Garage")
    UML_MANAGER._add_attribute("House", "Door")
    
    UML_MANAGER._add_class("Cat")
    UML_MANAGER._add_class("Dog")
    UML_MANAGER._add_class("Chicken")
    
    UML_MANAGER._add_relationship("Human", "Cat", "aggregation")
    UML_MANAGER._add_relationship("Human", "House", "composition")
    UML_MANAGER._add_relationship("Human", "Dog", "aggregation")
    UML_MANAGER._add_relationship("Dog", "Cat", "aggregation")

    
    
    # UML_MANAGER._load()
    # UML_MANAGER._display_class_list_detail()
    
    UML_MANAGER._save()
    


if __name__ == "__main__":
    main()
