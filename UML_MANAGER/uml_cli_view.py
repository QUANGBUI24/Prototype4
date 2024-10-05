###################################################################################################

from rich.console import Console
from rich.tree import Tree
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE
from enum import Enum
from typing import List, Dict
from UML_MANAGER.uml_observer import UMLObserver as Observer
from UML_MANAGER.uml_core_manager import InterfaceOptions 

###################################################################################################
### ENUM FOR RELATIONSHIP TYPE ###

class RelationshipType(Enum):
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"
    INHERITANCE = "inheritance"
    REALIZATION = "realization"

# UMLView class for displaying UML data
class UMLView(Observer):
    
    def __init__(self):
        self.console = Console()
    
    # UMLView class (the observer) updates data when user make changes
    def _update(self, event_type, data, is_loading: bool):
        # Add class #
        if event_type == InterfaceOptions.ADD_CLASS.value:
            class_name = data["class_name"]
            if not is_loading:
                self.console.print(f"\n[bold green]Class [bold white]'{class_name}'[/bold white] has been added.[/bold green]")
        # Delete class #
        elif event_type == InterfaceOptions.DELETE_CLASS.value:
            class_name = data.get('class_name', 'Unknown')
            self.console.print(f"\n[bold green]Class [bold white]'{class_name}'[/bold white] has been deleted.[/bold green]")
        # Rename class #
        elif event_type == InterfaceOptions.RENAME_CLASS.value:
            old_name = data["old_name"]
            new_name = data["new_name"]
            self.console.print(f"\n[bold green]Class [bold white]'{old_name}'[/bold white] has been renamed to [bold white]'{new_name}'[/bold white].[/bold green]")
        # Add field #
        elif event_type == InterfaceOptions.ADD_FIELD.value:
            class_name = data["class_name"]
            field_name = data["field_name"]
            if not is_loading:
                self.console.print(f"\n[bold green]Field [bold white]'{field_name}'[/bold white] has been added to class [bold white]'{class_name}'[/bold white].[/bold green]")
        # Delete field #
        elif event_type == InterfaceOptions.DELETE_FIELD.value:
            class_name = data["class_name"]
            field_name = data["field_name"]
            self.console.print(f"\n[bold green]Field [bold white]'{field_name}'[/bold white] has been deleted from class [bold white]'{class_name}'[/bold white].[/bold green]")
        # Rename field #
        elif event_type == InterfaceOptions.RENAME_FIELD.value:
            class_name = data["class_name"]
            old_field_name = data["old_field_name"]
            new_field_name = data["new_field_name"]
            self.console.print(f"\n[bold green]Field [bold white]'{old_field_name}'[/bold white] in class [bold white]'{class_name}'[/bold white] has been renamed to [bold white]'{new_field_name}'[/bold white].[/bold green]")
        # Add method #
        elif event_type == InterfaceOptions.ADD_METHOD.value:
            class_name = data["class_name"]
            method_name = data["method_name"]
            if not is_loading:
                self.console.print(f"\n[bold green]Successfully added method [bold white]'{method_name}'[/bold white] to class [bold white]'{class_name}'[/bold white]![/bold green]")
        # Delete method #
        elif event_type == InterfaceOptions.DELETE_METHOD.value:
            class_name = data["class_name"]
            method_name = data["method_name"]
            self.console.print(f"\n[bold green]Successfully removed method [bold white]'{method_name}'[/bold white] from class [bold white]'{class_name}'[/bold white]![/bold green]")
        # Rename method #
        elif event_type == InterfaceOptions.RENAME_METHOD.value:
            class_name = data["class_name"]
            old_method_name = data["old_method_name"]
            new_method_name = data["new_method_name"]
            self.console.print(f"\n[bold green]Successfully renamed from method [bold white]'{old_method_name}'[/bold white] to method [bold white]'{new_method_name}'[/bold white] from class [bold white]'{class_name}'[/bold white]![/bold green]")
        # Add parameter #
        elif event_type == InterfaceOptions.ADD_PARAM.value:
            class_name = data["class_name"]
            method_name = data["method_name"]
            param_name = data["param_name"]
            if not is_loading:
                self.console.print(f"\n[bold green]Successfully added parameter [bold white]'{param_name}'[/bold white] to method [bold white]'{method_name}'[/bold white] from class [bold white]'{class_name}'[/bold white]![/bold green]")
        # Delete parameter #
        elif event_type == InterfaceOptions.DELETE_PARAM.value:
            class_name = data["class_name"]
            method_name = data["method_name"]
            param_name = data["param_name"]
            self.console.print(f"\n[bold green]Successfully removed parameter [bold white]'{param_name}'[/bold white] from method [bold white]'{method_name}'[/bold white] from class [bold white]'{class_name}'[/bold white]![/bold green]")
        # Rename parameter #
        elif event_type == InterfaceOptions.RENAME_PARAM.value:
            class_name = data["class_name"]
            method_name = data["method_name"]
            old_param_name = data["old_param_name"]
            new_param_name = data["new_param_name"]
            self.console.print(f"\n[bold green]Successfully renamed from parameter [bold white]'{old_param_name}'[/bold white] to parameter [bold white]'{new_param_name}'[/bold white]![/bold green]")
        # Replace parameter #
        elif event_type == InterfaceOptions.REPLACE_PARAM.value:
            class_name = data["class_name"]
            method_name = data["method_name"]
            new_list = data["new_list"]
            self.console.print(f"\n[bold green]Successfully replaced parameter list for method [bold white]'{method_name}'[/bold white]![/bold green]")
        # Add relationship # 
        elif event_type == InterfaceOptions.ADD_REL.value:
            source_class = data["source"]
            destination_class = data["dest"]
            rel_type = data["type"]
            if not is_loading:
                self.console.print(f"\n[bold green]Successfully added relationship from class [bold white]'{source_class}'[/bold white] to class [bold white]'{destination_class}'[/bold white] of type '{rel_type}'![/bold green]")
        # Delete relationship # 
        elif event_type == InterfaceOptions.DELETE_REL.value:
            source_class = data["source"]
            destination_class = data["dest"]
            self.console.print(f"\n[bold green]Successfully removed relationship between class [bold white]'{source_class}'[/bold white] to class [bold white]'{destination_class}'[/bold white][/bold green]!") 
        # Change relationship type # 
        elif event_type == InterfaceOptions.TYPE_MOD.value:
            source_class = data["source"]
            destination_class = data["dest"]
            new_type = data["new_type"]
            self.console.print(f"\n[bold green]Successfully changed the type between class [bold white]'{source_class}'[/bold white] and class [bold white]'{destination_class}'[/bold white] to [bold white]'{new_type}'[/bold white]![/bold green]")
    
    # Get relationship type
    def _get_enum_list(self):
        return RelationshipType
        
    # Display the menu
    def _prompt_menu(self):
        banner = r"""[bold yellow]
    ▗▖ ▗▖▗▖  ▗▖▗▖       ▗▄▄▄▖▗▄▄▄ ▗▄▄▄▖▗▄▄▄▖▗▄▖ ▗▄▄▖ 
    ▐▌ ▐▌▐▛▚▞▜▌▐▌       ▐▌   ▐▌  █  █    █ ▐▌ ▐▌▐▌ ▐▌
    ▐▌ ▐▌▐▌  ▐▌▐▌       ▐▛▀▀▘▐▌  █  █    █ ▐▌ ▐▌▐▛▀▚▖
    ▝▚▄▞▘▐▌  ▐▌▐▙▄▄▖    ▐▙▄▄▖▐▙▄▄▀▗▄█▄▖  █ ▝▚▄▞▘▐▌ ▐▌
                                             
        
        Welcome to the UML Management Interface!
    For more information on commands, type "help" for the manual.
        [bold yellow]"""
        # Create a list of commands with their descriptions
        commands = [
            ["[bold yellow]Class Commands[/bold yellow]", ""],
            ["add_class [bright_white]<class_name>[bright_white]", "Add a new class"],
            ["delete_class [bright_white]<class_name>[bright_white]", "Delete an existing class"],
            ["rename_class [bright_white]<class_name> <new_name>[bright_white]", "Rename a class"],

            ["[bold yellow]Field Commands[/bold yellow]", ""],
            ["add_field [bright_white]<class_name> <attr_name>[bright_white]", "Add a field to a class"],
            ["delete_field [bright_white]<class_name> <field_name>[bright_white]", "Delete a field from a class"],
            ["rename_field [bright_white]<class_name> <current_field_name> <new_name>[bright_white]", "Rename a field"],

            ["[bold yellow]Method Commands[/bold yellow]", ""],
            ["add_method [bright_white]<class_name> <method_name>[bright_white]", "Add a method to a class"],
            ["delete_method [bright_white]<class_name> <method_name>[bright_white]", "Delete a method from a class"],
            ["rename_method [bright_white]<class_name> <current_method_name> <new_name>[bright_white]", "Rename a method"],

            ["[bold yellow]Parameter Commands[/bold yellow]", ""],
            ["add_param [bright_white]<class_name> <method_name> <param_name>[bright_white]", "Add a parameter to a method"],
            ["delete_param [bright_white]<class_name> <method_name> <param_name>[bright_white]", "Delete a parameter from a method"],
            ["rename_param [bright_white]<class_name> <method_name> <current_param_name> <new_name>[bright_white]", "Rename a parameter"],
            ["replace_param [bright_white]<class_name> <method_name>[bright_white]", "Replace a method's parameter list"],

            ["[bold yellow]Relationship Commands[/bold yellow]", ""],
            ["add_rel [bright_white]<source_class> <destination_class> <relationship_type>[bright_white]", "Add a relationship between two classes"],
            ["delete_rel [bright_white]<source_class> <destination_class>[bright_white]", "Delete a relationship between two classes"],
            ["type_mod [bright_white]<source_class> <destination_class> <type>[bright_white]", "Modify the type of a relationship"],

            ["[bold yellow]Class-Related Commands[/bold yellow]", ""],
            ["list_class", "List all created classes"],
            ["class_detail [bright_white]<class_name>[bright_white]", "View details of a specific class"],
            ["class_rel", "View relationships between classes"],

            ["[bold yellow]Save/Load Commands[/bold yellow]", ""],
            ["saved_list", "List all saved files"],
            ["save", "Save current data"],
            ["load", "Load data from a saved file"],
            ["delete_saved", "Delete a saved file"],
            ["clear_data", "Clear all data from current storage"],
            ["default", "Reset to a blank program"],

            ["[bold yellow]Other Commands[/bold yellow]", ""],
            ["sort", "Sort the class list alphabetically"],
            ["help", "View instructions"],
            ["exit", "Exit the program"]
        ]
        # Create a table to organize commands and descriptions
        table = Table(title=banner, show_header=True, header_style="bold yellow", border_style="bold dodger_blue2", box=SQUARE)
        table.add_column(f"{'Command':^75}", style="bold dodger_blue2", justify="left", no_wrap=True)
        table.add_column(f"{'Description':^45}", style="bold bold white")
        # Add rows to the table
        for command, description in commands:
            table.add_row(command, description)
        # Create a panel to wrap the table with a welcome message
        panel = Panel.fit(table, border_style="bold dodger_blue2")
        # Print the panel with the commands
        self.console.print(panel)
        
    def _display_wrapper(self, main_data: Dict):
        if len(main_data["classes"]) == 0:
            self.console.print("\n[bold red]No class to display![/bold red]")
            return
        is_detail = self._ask_user_choices("print all class detail")
        if is_detail:
            self._display_uml_data(main_data)
        else:
            self._display_class_names(main_data)

    # Display all class detail
    def _display_uml_data(self, main_data: Dict):
        # Main tree to hold UML structure
        tree = Tree("\nUML Classes and Relationships")
        # Add classes to the tree
        classes_tree = tree.add("Classes")
        for cls in main_data["classes"]:
            class_branch = classes_tree.add(f'[bold green]{cls["name"]}[/bold green]')
            self._display_class(class_branch, cls)
        # Add relationships to the tree
        relationships_tree = tree.add("Relationships")
        for relation in main_data["relationships"]:
            relationships_tree.add(
                f'[bold dodger_blue2]{relation["source"]}[/bold dodger_blue2] [bold white]--{relation["type"]}-->[bold white] [bold dodger_blue2]{relation["destination"]}[/bold dodger_blue2]'
            )
        # Print the complete tree
        self.console.print(tree)

    # Structure the class detail into branches
    def _display_class(self, class_branch, cls):
        # Add fields of the class
        fields_branch = class_branch.add("[bold yellow]Fields[/bold yellow]")
        for field in cls["fields"]:
            fields_branch.add(f'[bold dark_slate_gray2]{field["name"]}[/bold dark_slate_gray2]')
        # Add methods of the class
        methods_branch = class_branch.add("[bold yellow]Methods[/bold yellow]")
        for method in cls["methods"]:
            # Extract the names of the parameters
            params = ', '.join(param["name"] for param in method["params"])
            methods_branch.add(f'[bold dark_orange]{method["name"]}([bold slate_blue1]{params}[/bold slate_blue1])[/bold dark_orange]')
    
    # Display class names
    def _display_class_names(self, main_data: Dict):
        # Create a table to display all class names
        table = Table(title="\n[bold white]Class Names[/bold white]", show_header=True, header_style="bold yellow", border_style="bold dodger_blue2")
        table.add_column("Class Name", justify="center", style="bold white")
        # Iterate through all classes and add their names to the table
        for cls in main_data["classes"]:
            table.add_row(cls["name"])
        # Print the table with the class names
        self.console.print(table)
        
    # Display single class detail
    def _display_single_class(self, class_name: str, main_data: Dict):
        # Main tree to hold UML structure
        tree = Tree("\nUML Classes and Relationships")
        # Add classes to the tree
        classes_tree = tree.add("Class")
        for cls in main_data["classes"]:
            if cls["name"] == class_name:
                class_branch = classes_tree.add(f'[bold green]{cls["name"]}[/bold green]')
                self._display_class(class_branch, cls)
        # Add relationships to the tree
        relationships_tree = tree.add("Relationships")
        for relation in main_data["relationships"]:
            if relation["source"] == class_name or relation["destination"] == class_name:
                relationships_tree.add(
                    f'[bold dodger_blue2]{relation["source"]}[/bold dodger_blue2] [bold white]--{relation["type"]}-->[/bold white] [bold dodger_blue2]{relation["destination"]}[/bold dodger_blue2]'
                )
        # Print the complete tree
        self.console.print(tree)
        
    # Display relationship
    def _display_relationships(self, main_data):
        # Create a table to display all relationships
        table = Table(title="\n[bold white]Relationships[/bold white]", show_header=True, header_style="bold yellow", border_style="bold dodger_blue2")
        table.add_column("Source Class", style="bold white")
        table.add_column("Relationship Type", style="bold green")
        table.add_column("Destination Class", style="bold white")
        # Iterate through all relationships and add them to the table
        for relation in main_data["relationships"]:
            table.add_row(
                relation["source"],
                relation["type"],
                relation["destination"]
            )
        # Print the table with relationships
        self.console.print(table)
    
    # Display type for relationship
    def _display_type_enum(self):
        # Create a table to display relationship types
        table = Table(title="\n[bold white]Relationship Types[/bold white]", show_header=True, header_style="bold yellow", border_style="bold dodger_blue2")
        table.add_column("Type", justify="center", style="bold white")
        # Iterate through the RelationshipType enum and add each type to the table
        for type_ in RelationshipType:
            table.add_row(type_.value)
        # Print the table with the relationship types
        self.console.print(table)
        
    # Display saved file's names using Rich
    def _display_saved_list(self, saved_list: List):
        # Check if there are any saved files
        if len(saved_list) == 0:
            self.console.print("\n[bold red]No saved file exists![/bold red]")
            return
        # Create a table to display saved file names
        table = Table(title="\n[bold white]Saved Files[bold white]", show_header=True, header_style="bold yellow", border_style="bold dodger_blue2")
        table.add_column("File Name", justify="center", style="bold white")
        # Iterate through saved_list and add each file name to the table
        for dictionary in saved_list:
            for key in dictionary:
                table.add_row(key)
        # Print the table with saved file names
        self.console.print(table)
            
    # Ask For User Choices #
    def _ask_user_choices(self, action: str) -> bool:
        while True:
            self.console.print(f"\n[bold yellow]Do you want to {action}? (Yes/No): [bold yellow]")
            user_input = input().lower()
            if user_input in ["yes", "y"]:
                return True
            elif user_input in ["no", "n"]:
                return False
            else:
                print("Invalid input. Please enter 'Yes' or 'No'.")
                
################################################################################################### 
            