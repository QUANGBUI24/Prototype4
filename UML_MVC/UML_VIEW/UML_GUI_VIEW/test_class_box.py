from PyQt5 import QtWidgets, QtGui, QtCore

class UMLTestBox(QtWidgets.QGraphicsRectItem):
    def __init__(self, interface, class_name="ClassName", field=None, methods=None, parent=None):
         # Interface to communicate with UMLCoreManager
        self.interface = interface  
        
        # Default properties for attributes (fields) and methods if not provided
        self.field = field if field is not None else []
        self.methods = methods if methods is not None else []