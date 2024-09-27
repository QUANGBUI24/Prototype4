from UML_INTERFACE.uml_cli_interface import UMLCommandLineInterface as Interface  

def main():
    program_interface = Interface()
    program_interface.main_program_loop()

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
