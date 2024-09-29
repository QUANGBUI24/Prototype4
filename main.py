from UML_INTERFACE.uml_cli_interface import UMLCommandLineInterface as Interface  

# from rich.table import Table
# from rich.console import Console
# console = Console()

# def test_format(class_data):
#     for class_element in class_data:
#         # Create a new table for each class
#         table = Table(title=f"Class: {class_element['classes']}")
#         table.add_column("Fields", style="green")
#         table.add_column("Methods", style="cyan")
#         table.add_column("Parameters", style="magenta")
#         # Add rows with fields, methods, and parameters
#         fields_str = ", ".join(class_element["fields"])
#     for method in class_element["methods"]:
#         method_name = method["method_name"]
#         params_str = ", ".join(method["params"])
#         table.add_row(fields_str, method_name, params_str)
#     console.print(table)
    
# def new_test_format(class_data):
#     for class_element in class_data:
#         pass

def main():
    program_interface = Interface()
    program_interface.main_program_loop()
    
if __name__ == "__main__":
    main()
