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
        # Figure and subplot
        fig = self.create_figure()
        
        super(MplCanvas, self).__init__(fig)


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
        
        # Figure title
        fig.suptitle(title, fontsize=20, x=0.5, y=0.91)
        
        return fig


    def create_subplot(self, axes_names: tuple, y_axis_position=0) -> plt.Axes:
        """Creates customized subplot.

        Args:
            fig (plt.Figure): figure, where to plot.
            axes_names (tuple): names for Ox and Oy axes.
            y_axis_position (int, optional): postion of Oy axis in plot (data wise). Defaults to 0.

        Returns:
            plt.Axes: generated subplot.
        """
        
        # Subplot init
        subplot = self.figure.add_subplot()
        
        # Move Ox line at 0
        subplot.spines['bottom'].set_position(('data', 0))
        # Move Oy line at provided position
        subplot.spines['left'].set_position(('data', y_axis_position))
        
        # Hide the top and right spines.
        subplot.spines[['top', 'right']].set_visible(False)
        
        # Draw arrows (as black triangles: ">k"/"^k") at the end of the axes.  In each
        # case, one of the coordinates (0) is a data coordinate (i.e., y = 0 or x = 0,
        # respectively) and the other one (1) is an axes coordinate (i.e., at the very
        # right/top of the axes).  Also, disable clipping (clip_on=False) as the marker
        # actually spills out of the axes.
        # Ox arrow:
        subplot.plot(1, 0, '>k', transform=subplot.get_yaxis_transform(), clip_on=False)
        # Oy arrow:
        subplot.plot(y_axis_position, 1, '^k', transform=subplot.get_xaxis_transform(), clip_on=False)
        
        # Ox and Oy tick labels size
        subplot.tick_params(axis='both', which='major', labelsize=20)
        
        # Hide Oy zero label
        subplot.yaxis.get_major_ticks()[1].label1.set_visible(False)
        
        # Align Ox labels to the right of the ticks
        for label in subplot.get_xticklabels():
            label.set_horizontalalignment('left')
        self.figure.align_xlabels()
        
        # Axes labels name, location and rotation
        subplot.set_xlabel(axes_names[0], loc='right', fontsize=20)
        subplot.set_ylabel(axes_names[1], loc='top', rotation=0, fontsize=20)
        
        return subplot


    class FuncToPlot1D:
        """Stores info about 1d function.
        """
        
        def __init__(self, x: ndarray, y: ndarray, legend_name: str, style=None):
            # X points
            self.x = x
            # Y points
            self.y = y
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
        
        # Collect all minimum X positions
        mins = np.empty((len(functions)))
        for i in range(len(functions)):
            mins[i] = functions[i].x[0]
        # Y axis position is at 0 or minimum value of combined grid
        y_axis_position=max(0, np.min(mins))
        
        # Init subplot
        subplot = self.create_subplot((x_axis_name, ''), y_axis_position)
        
        # Plot data
        for function in functions:
            if function.style == None:
                subplot.plot(function.x, function.y, label=function.legend_name)
            else:
                subplot.plot(function.x, function.y, function.style, label=function.legend_name)
        
        # Show legend  
        subplot.legend(fontsize=20, loc='upper right')