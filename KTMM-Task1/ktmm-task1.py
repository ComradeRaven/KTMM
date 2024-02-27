###########
# IMPORTS #
###########


# System
import sys
# UI
from PyQt6 import QtWidgets
# Custom modules
from lib.classes.ui import MainWindow


###########
# Program #
###########


app = QtWidgets.QApplication(sys.argv)

# Dark app theme
app.setStyle("fusion")

w = MainWindow()

# Run app cycle
app.exec()