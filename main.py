from UML_INTERFACE.uml_core_manager_interface import UMLInterface as Interface  
from UML_MANAGER.uml_cli_view import UMLView as View

def main():
    view = View()
    interface = Interface(view)
    interface.attach_observer(view)
    interface.main_program_loop()
    interface.detach_observer(view)
    
if __name__ == "__main__":
    main()
