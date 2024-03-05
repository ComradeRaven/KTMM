###########
# IMPORTS #
###########


# Handy arrays
import numpy as np
# Plotting
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# For annotations
from numpy import ndarray


###################
# Canvas for plot #
###################


class MplCanvas(FigureCanvas):

    def __init__(self):
        # Figure
        fig, subplot = self.create_figure()
        
        super(MplCanvas, self).__init__(fig)
        
        self.subplot = subplot


    def create_figure(self, title='') -> tuple[plt.Figure, plt.Axes]:
        """Creates customized plot.

        Args:
            title (str, optional): plot title. Defaults to ''.
            x_axis_name (str, optional): name for Ox axis. Defaults to ''.

        Returns:
            tuple[plt.Figure, plt.Axes]: generated figure and its subplot.
        """
        
        # Init figure
        fig = plt.figure(figsize=(20, 10))
        
        fig, subplot = plt.subplot_mosaic([['bottom', 'bottom', 'bottom', 'bottom', 'bottom', 'BLANK']],
                                          empty_sentinel="BLANK", figsize=(30, 15))
        
        # Figure title
        fig.suptitle(title, fontsize=20, x=0.5, y=0.91)
        
        # Select subplot
        subplot = subplot['bottom']
        
        # Hide the top and right spines.
        subplot.spines[['top', 'right']].set_visible(False)
        
        # Ox and Oy tick labels size
        subplot.tick_params(axis='both', which='major', labelsize=20)
        
        return fig, subplot


    class FuncToPlot1D:
        """Stores info about 1d function.
        """
        
        def __init__(self, x: ndarray, f: ndarray, legend_name: str, style=None):
            # X points
            self.x = x
            # Y points
            self.f = f
            # Name in the legend
            self.legend_name = legend_name
            # Line style (string)
            self.style = style


    def plot_functions(self, functions: list[FuncToPlot1D], x_axis_name='') -> None:
        """Shows given functions in the same plot.

        Args:
            functions (list[FuncToPlot1D]): functions to plot.
            title (str, optional): plot title. Defaults to ''.
            x_axis_name (str, optional): name for Ox axis. Defaults to ''.
        """
        
        # Collect all minimum X and Y positions
        x_mins, y_mins = np.empty((len(functions))), np.empty((len(functions)))
        for i in range(len(functions)):
            x_mins[i] = functions[i].x[0]
            y_mins[i] = functions[i].f[0]
        # Y axis position is at minimum value of combined grid
        y_axis_position = np.min(x_mins)
        # X axis position is at minimum value of all functions
        x_axis_position = np.min(y_mins)
        
        # Move Ox line at 0
        self.subplot.spines['bottom'].set_position(('data', x_axis_position))
        # Move Oy line at provided position
        self.subplot.spines['left'].set_position(('data', y_axis_position))
        
        # Align Ox tick labels to the right of the ticks
        for label in self.subplot.get_xticklabels():
            label.set_horizontalalignment('left')
        self.figure.align_xlabels()
        # Align Oy tick labels above the ticks
        for label in self.subplot.get_yticklabels():
            label.set_verticalalignment('bottom')
        self.figure.align_ylabels()
        
        # Axes labels name, location and rotation
        self.subplot.set_xlabel(x_axis_name, loc='right', fontsize=20)
        self.subplot.set_ylabel('', loc='top', rotation=0, fontsize=20)
        
        # Plot data
        for function in functions:
            if function.style == None:
                self.subplot.plot(function.x, function.f, label=function.legend_name)
            else:
                self.subplot.plot(function.x, function.f, function.style, label=function.legend_name)
        
        # Grid
        self.subplot.grid()
        # Legend  
        self.subplot.legend(fontsize=20, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)