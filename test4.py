from PyQt5 import QtWidgets, QtPrintSupport

def export_to_pdf(widget):
    # Create a printer object
    printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
    
    # Set output file name for PDF
    printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
    printer.setOutputFileName("output.pdf")
    
    # Render the widget into the PDF file
    widget.render(printer)

# Example usage (assuming 'widget' is your QWidget)
app = QtWidgets.QApplication([])
window = QtWidgets.QWidget()
export_to_pdf(window)
