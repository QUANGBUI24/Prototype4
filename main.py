from UML_INTERFACE.uml_cli_interface import UMLCommandLineInterface as Interface  

from rich.table import Table
from rich.console import Console
console = Console()

def test_format(class_data):
    for class_element in class_data:
        # Create a new table for each class
        table = Table(title=f"Class: {class_element['class_name']}")
        table.add_column("Fields", style="green")
        table.add_column("Methods", style="cyan")
        table.add_column("Parameters", style="magenta")
        # Add rows with fields, methods, and parameters
        fields_str = ", ".join(class_element["fields"])
    for method in class_element["methods"]:
        method_name = method["method_name"]
        params_str = ", ".join(method["params"])
        table.add_row(fields_str, method_name, params_str)
    console.print(table)

def main():
    program_interface = Interface()
    # program_interface.main_program_loop()
    program_interface.load()
    main_data = program_interface.get_main_data()
    
    print(main_data)
    
    # class_data = main_data["classes"]
    # test_format(class_data)
    
    

    # program_interface.add_class("Human")
    # program_interface.add_method("Human", "Attack")
    # # program_interface.add_method("Human", "Run")
    # # program_interface.add_method("Human", "Walk")
    # program_interface.add_parameter("Human", "Attack", "Damage")
    # program_interface.add_parameter("Human", "Attack", "Critical_Rate")
    # program_interface.add_parameter("Human", "Attack", "Element")
    # # program_interface.add_parameter("Human", "Run", "Speed")
    # # program_interface.add_parameter("Human", "Run", "Initial_Velocity")
    # # program_interface.add_parameter("Human", "Walk", "WSpeed")
    # # program_interface.add_parameter("Human", "Walk", "WInitial_Velocity")
    # program_interface.display_classes()
    # program_interface.replace_param_list("Human", "Attack")
    # program_interface.display_classes()
    
    # # get_list = program_interface.get_method_and_parameter_list("Human")
    # # param_list = get_list["Attack"]
    # # for ele in param_list:
    # #    print(ele._get_parameter_name())

if __name__ == "__main__":
    main()
