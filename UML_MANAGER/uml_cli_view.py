from rich.console import Console
from rich.tree import Tree
from rich.table import Table

# Initialize Rich Console
console = Console()

# UMLView class for displaying UML data
class UMLView:

    def __init__(self):
        self.console = console
        
    def _display_wrapper(self, main_data):
        # if len(self.__class_list) == 0:
        #     print("\nNo class to display!")
        #     return
        is_detail = self._ask_user_choices("print all class detail")
        if is_detail:
            self._display_uml_data()
        else:
            self.__display_list_of_only_class_name()

    def _display_uml_data(self, data):
        # Main tree to hold UML structure
        tree = Tree("UML Classes and Relationships")

        # Add classes to the tree
        classes_tree = tree.add("Classes")
        for cls in data["classes"]:
            class_branch = classes_tree.add(f'[bold green]{cls["name"]}[/bold green]')
            self._display_class(class_branch, cls)

        # Add relationships to the tree
        relationships_tree = tree.add("Relationships")
        for relation in data["relationships"]:
            relationships_tree.add(
                f'[bold blue]{relation["source"]}[/bold blue] --{relation["type"]}--> [bold blue]{relation["destination"]}[/bold blue]'
            )

        # Print the complete tree
        self.console.print(tree)

    def _display_class(self, class_branch, cls):
        # Add fields of the class
        fields_branch = class_branch.add("[yellow]Fields[/yellow]")
        for field in cls["fields"]:
            fields_branch.add(f'[cyan]{field["name"]}[/cyan]')

        # Add methods of the class
        methods_branch = class_branch.add("[yellow]Methods[/yellow]")
        for method in cls["methods"]:
            # Extract the names of the parameters
            params = ', '.join(param["name"] for param in method["params"])
            methods_branch.add(f'[magenta]{method["name"]}({params})[/magenta]')
    
    def _display_class_names(self, data):
        # Create a table to display all class names
        table = Table(title="Class Names", show_header=True, header_style="bold yellow")
        table.add_column("Class Name", justify="center", style="bold cyan")

        # Iterate through all classes and add their names to the table
        for cls in data["classes"]:
            table.add_row(cls["name"])

        # Print the table with the class names
        self.console.print(table)
            
    # Ask For User Choices #
    def _ask_user_choices(self, action: str) -> bool:
        while True:
            user_input = input(f"\nDo you want to {action}? (Yes/No): ").lower()
            if user_input in ["yes", "y"]:
                return True
            elif user_input in ["no", "n"]:
                return False
            else:
                print("Invalid input. Please enter 'Yes' or 'No'.")
                