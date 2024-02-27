###########
# IMPORTS #
###########


# Handy arrays
import numpy as np
# System
import sys
# UI
from PyQt6 import QtCore, QtWidgets
# Custom modules
import lib.utils as Utils
from lib.classes.mesh import Mesh


###########
# Program #
###########

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        filepath = 'model/model1.obj'

        self.mesh = Mesh(filepath)
        
        self.show()

        print('vertex array shape: ', self.mesh.vertices.shape)
        print('Mesh parts surfaces:')
        print(self.mesh.surfaces)
        print('Intersections surfaces:')
        print(self.mesh.intercestions_surfaces)

# Run app
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()