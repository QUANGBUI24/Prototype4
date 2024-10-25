class Command:
    """
    Command interface with execute and undo methods.
    """
    def execute(self):
        raise NotImplementedError("Execute method must be implemented.")

    def undo(self):
        raise NotImplementedError("Undo method must be implemented.")


class TextEditor:
    """
    A simple text editor class that stores the current text.
    """
    def __init__(self):
        self.text = ""

    def add_text(self, new_text: str):
        self.text += new_text

    def remove_text(self, length: int):
        self.text = self.text[:-length]

    def __str__(self):
        return self.text


class AddTextCommand(Command):
    """
    Command to add text to the text editor.
    """
    def __init__(self, editor: TextEditor, text_to_add: str):
        self.editor = editor
        self.text_to_add = text_to_add

    def execute(self):
        """
        Adds the specified text to the text editor.
        """
        self.editor.add_text(self.text_to_add)

    def undo(self):
        """
        Removes the added text from the text editor (undo).
        """
        self.editor.remove_text(len(self.text_to_add))


class CommandManager:
    """
    Manages the commands for undo and redo operations.
    """
    def __init__(self):
        self.undo_stack = []  # Stack for undo commands
        self.redo_stack = []  # Stack for redo commands

    def execute_command(self, command: Command):
        """
        Executes a command and stores it in the undo stack.
        Clears the redo stack when a new command is executed.
        """
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()  # Clear redo stack when a new command is executed

    def undo(self):
        """
        Undoes the last executed command.
        """
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)
        else:
            print("Nothing to undo.")

    def redo(self):
        """
        Redoes the last undone command.
        """
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.undo_stack.append(command)
        else:
            print("Nothing to redo.")


def main():
    editor = TextEditor()
    command_manager = CommandManager()

    # Simulate adding text
    command_manager.execute_command(AddTextCommand(editor, "Hello, "))
    print(f"Editor content: {editor}")

    command_manager.execute_command(AddTextCommand(editor, "World!"))
    print(f"Editor content: {editor}")

    # Undo last command
    command_manager.undo()
    print(f"Editor content after undo: {editor}")

    # Redo last undone command
    command_manager.redo()
    print(f"Editor content after redo: {editor}")

    # Add more text
    command_manager.execute_command(AddTextCommand(editor, " How are you?"))
    print(f"Editor content: {editor}")

    # Undo twice
    command_manager.undo()
    print(f"Editor content after undo: {editor}")

    command_manager.undo()
    print(f"Editor content after second undo: {editor}")

    # Redo
    command_manager.redo()
    print(f"Editor content after redo: {editor}")


if __name__ == "__main__":
    main()
