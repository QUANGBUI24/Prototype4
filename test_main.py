# main.py

import sys
from PyQt5.QtWidgets import QApplication
from UML_MANAGER.uml_core_manager import UMLCoreManager
from observer_gui_test import UMLGui

def main():
    app = QApplication(sys.argv)
    core_manager = UMLCoreManager()
    gui = UMLGui(core_manager)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
