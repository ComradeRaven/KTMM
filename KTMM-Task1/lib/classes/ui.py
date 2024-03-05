###########
# IMPORTS #
###########


# Handy arrays
import numpy as np
# .json files
import json
# UI
from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6.QtGui import QAction
# Custom modules
import lib.utils as utils
from lib.classes.mesh import Mesh
from lib.classes.config import Config
from lib.classes.plotting import MplCanvas

# For annotations
from numpy import ndarray


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
        
        # Animation button
        self.button_anim = QtWidgets.QPushButton("Start")
        self.button_anim.clicked.connect(self.on_anim_button_click)
        # Disable button for now
        self.button_anim.setEnabled(False)
        
        # Grid layout
        self.grid = QtWidgets.QGridLayout()
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.grid)
        self.setCentralWidget(self.central_widget)
        # Add wigets to grid
        self.grid.addWidget(self.plot, 0, 0)
        self.grid.addWidget(self.button_anim, 1, 0)
        
        # Timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.solve)
        self.timer_isactive = False
        
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
                if {'eps', 'c', 'lambda', 'Q_R', 'y0', 't'} <= config.keys():
                    
                    # Save config
                    self.config = Config(config['eps'], config['c'], config['lambda'], config['Q_R'], config['y0'], config['t'])
                    
                    # Debug
                    print('Loaded config: ',
                          self.config.eps,
                          self.config.c,
                          self.config.therm_cond_coefs,
                          self.config.q_r,
                          self.config.y0,
                          self.config.t)
                    
                    # Solve ODE
                    self.time_interval = eval(self.config.t, globals(), locals())
                    self.y0 = self.config.y0
                    odeinit_output = self.solve()
                    
                    # Save .csv file
                    np.savetxt('output.csv', odeinit_output, delimiter = ",")
                    
                    # Enable animation button
                    self.button_anim.setDisabled(False)
                    
                # Invalid data
                else:
                    QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid config file contents')
    
    
    def on_anim_button_click(self):
        """Starts or stops animation."""
        
        if self.timer_isactive:
            self.timer_isactive = False
            self.button_anim.setText('Start')
            self.timer.stop()
        else:
            self.timer_isactive = True
            self.button_anim.setText('Stop')
            self.timer.start()
        
    
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
    
    
    def solve(self):
        """Solves equation with current data.
        """
        
        # Calculate temperatures
        odeinit_output = utils.calculate_temperatures(self.mesh, self.config, self.y0, self.time_interval)
        # Plot
        self.plot_data(odeinit_output)
        
        # Update time interval
        self.time_interval += 5
        # Update boundary condition
        self.y0 = odeinit_output[1, :]
        
        return odeinit_output
    
    
    def plot_data(self, odeinit_output: ndarray) -> None:
        """Plots provided data on canvas..
        """
        
        # Construct functions list
        functions = []
        for i in range(odeinit_output.shape[1]):
            functions.append(MplCanvas.FuncToPlot1D(self.time_interval, odeinit_output[:, i], r'$T_{y_num}$'.format(y_num=i)))
        
        # Clear figure
        self.plot.subplot.cla()
        # Plot data
        self.plot.plot_functions(functions, 't')
        self.plot.draw()