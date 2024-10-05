from UML_INTERFACE.uml_core_manager_interface import UMLInterface as Interface  
from UML_VIEW.uml_cli_view import UMLView as CLIView
from UML_VIEW.uml_gui_view import MainWindow as GUIView
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QLabel
import sys

def main():
    # interface = Interface()
    # view = CLIView()
    # interface.attach_observer(view)
    # interface.main_program_loop()
    # interface.detach_observer(view)
    
    app = QApplication(sys.argv)
    interface = Interface()
    storage = interface.get_storage_manager()
    # Console View
    console_view = CLIView()
    interface.attach_observer(console_view)
    # GUI View
    gui_view = GUIView(interface)  # Pass the interface to the GUI view
    interface.attach_observer(gui_view)
    # Show GUI
    gui_view.show()
    # Start main loop
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
