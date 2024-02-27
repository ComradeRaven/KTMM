###########
# IMPORTS #
###########


# .json files
import json
# UI
from PyQt6 import QtWidgets
from PyQt6.QtGui import QAction
# Custom modules
from lib.classes.mesh import Mesh


###################
# App main window #
###################


class MainWindow(QtWidgets.QMainWindow):
    """Defines app main window."""
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # App title
        self.setWindowTitle('KTMM-Task1')
        
        # Toolbar
        toolbar = QtWidgets.QToolBar('Toolbar')
        self.addToolBar(toolbar)
        # Config button
        button_config = QAction('Config', self)
        button_config.triggered.connect(self.onConfigButtonClick)
        toolbar.addAction(button_config)
        
        # Show App window
        self.show()
        
        # Load model
        filepath = 'model/model1.obj'
        self.mesh = Mesh(filepath)
        
        # Debug
        print('vertex array shape: ', self.mesh.vertices.shape)
        print('Mesh parts surfaces:')
        print(self.mesh.surfaces)
        print('Intersections surfaces:')
        print(self.mesh.intercestions_surfaces)
    
    
    def onConfigButtonClick(self, s):
        """Handles config button click event."""
        
        # Open file selection dialog
        dialog = QtWidgets.QFileDialog(self)
        dialog.setNameFilter("Images (*.json)")
        # Gather selected files
        filenames = []
        if dialog.exec():
            filenames = dialog.selectedFiles()
        
        # Open file and try to parse .json
        if len(filenames) > 0:
            with open(filenames[0]) as f:
                config = json.load(f)
                
                # Check keys
                if {'eps1', 'eps2', 'eps3', 'eps4', 'eps5',
                    'c1', 'c2', 'c3', 'c4', 'c5',
                    'lambda_12', 'lambda_23', 'lambda_34', 'lambda_12', 'lambda_45'} <= config.keys():
                    
                    # save data
                    eps = [config['eps1'], config['eps2'], config['eps3'], config['eps4'], config['eps5']]
                    c = [config['c1'], config['c2'], config['c3'], config['c4'], config['c5']]
                    print(eps, c)

                # Invalid data
                else:
                    QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid config file contents')