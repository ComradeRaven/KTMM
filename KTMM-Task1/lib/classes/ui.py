###########
# IMPORTS #
###########


# .json files
import json
# UI
from PyQt6 import QtWidgets
from PyQt6.QtGui import QAction
# Custom modules
import lib.utils as utils
from lib.classes.mesh import Mesh
from lib.classes.config import Config
from lib.classes.plotting import MplCanvas


###################
# App main window #
###################


class MainWindow(QtWidgets.QMainWindow):
    """Defines app main window.
    """
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # App title
        self.setWindowTitle('KTMM-Task1')
        
        # Toolbar
        toolbar = QtWidgets.QToolBar('Toolbar')
        self.addToolBar(toolbar)
        
        # Mesh button
        button_mesh = QAction('Mesh', self)
        button_mesh.triggered.connect(self.on_mesh_button_click)
        toolbar.addAction(button_mesh)
        # Set empty mesh
        self.mesh = None
        
        # Config button
        self.button_config = QAction('Config', self)
        self.button_config.triggered.connect(self.on_config_button_click)
        toolbar.addAction(self.button_config)
        # Disable button for now
        self.button_config.setEnabled(False)
        # Set empty config
        self.config = None
        
        # Plot canvas
        self.plot = MplCanvas()
        self.setCentralWidget(self.plot)
        
        # Show App window
        self.show()
    
    
    def on_mesh_button_click(self, s) -> None:
        """Handles mesh button click event.
        """
        
        # Ask to select mesh file
        filename = self.open_file_dialog("Mesh (*.obj)")
        
        if filename != None:
            # Load model
            self.mesh = Mesh(filename)
            
            # Enable config button
            self.button_config.setDisabled(False)
            
            # Debug
            print('Vertex array shape: ', self.mesh.vertices.shape)
            print('Mesh parts surfaces:', self.mesh.surfaces)
            print('Intersections surfaces:', self.mesh.intercestions_surfaces)
    
    
    def on_config_button_click(self, s) -> None:
        """Handles config button click event.
        """
        
        # Ask to select config file
        filename = self.open_file_dialog("Config (*.json)")
        
        # Open file and try to parse .json
        if filename != None:
            with open(filename) as f:
                config = json.load(f)
                
                # Check keys
                if {'eps', 'c', 'lambda', 'Q_R'} <= config.keys():
                    
                    # Save config
                    self.config = Config(config['eps'], config['c'], config['lambda'], config['Q_R'])
                    
                    # Debug
                    print('Loaded config: ', self.config.eps, self.config.c, self.config.therm_cond_coefs, self.config.q_r)
                    
                    # Calculate temperatures
                    t, y = utils.calculate_temperatures(self.mesh, self.config)
                    # Plot
                    funcs_to_plot = []
                    for i in range(len(y)):
                        funcs_to_plot.append(MplCanvas.FuncToPlot1D(t, y[i], r'$elem_{y_num}$'.format(y_num=i)))
                    self.plot_data(funcs_to_plot)

                # Invalid data
                else:
                    QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid config file contents')
    
    
    def open_file_dialog(self, name_filter: str):
        """Opens a dialog for selecting a single file with provided extension.

        Args:
            name_filter (str): file extension filtering.

        Returns:
            _type_: filename.
        """
        
        # Open file selection dialog
        dialog = QtWidgets.QFileDialog(self)
        dialog.setNameFilter(name_filter)
        # Single file selection
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        
        # Gather selected files
        filenames = []
        if dialog.exec():
            filenames = dialog.selectedFiles()
        
        # File was selected
        if len(filenames) > 0:
            return filenames[0]
        # Nothing was selected
        else:
            return None
    
    
    def plot_data(self, functions) -> None:
        """Plots provided data on canvas.

        Args:
            functions (list, optional): functions to plot.
        """
        
        # Clear figure
        self.plot.figure.clf()
        # Plot data
        self.plot.plot_functions(functions, 't')
        self.plot.draw()