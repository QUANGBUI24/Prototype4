import readline

# List of possible commands for tab completion
COMMANDS = ['start', 'stop', 'restart', 'status', 'help', 'exit']

def completer(text, state):
    """
    This function is called every time tab is pressed.
    It matches the input text with the available commands.
    """
    options = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    return None

def main():
    # Enable tab completion
    readline.parse_and_bind("tab: complete")
    
    # Set the completer function
    readline.set_completer(completer)
    
    while True:
        # Input prompt
        user_input = input('Command> ').strip()

        # If user types 'exit', break the loop
        if user_input == 'exit':
            break

        # If the command is valid, display it
        elif user_input in COMMANDS:
            print(f'Executing command: {user_input}')
        else:
            print(f'Unknown command: {user_input}')

if __name__ == '__main__':
    main()
