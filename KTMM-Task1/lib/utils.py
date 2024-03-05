###########
# IMPORTS #
###########


# Math
import math
# Handy arrays
import numpy as np
# ODE solver
import scipy.integrate as integrate
# Custom modules
from lib.classes.mesh import Mesh
from lib.classes.config import Config
from lib.classes.eq_eval import EquationEvaluator

# For annotations
from numpy import ndarray


#########
# Utils #
#########


def triangle_surface(vertices: ndarray) -> float:
    """Calculates triangle surface in 3D space.
    """
    
    # Parallelogram vectors
    vector1 = vertices[1] - vertices[0]
    vector2 = vertices[2] - vertices[0]
    
    # Cross product
    cross = np.cross(vector1, vector2)
    
    # Half of the module of the cross product
    return math.sqrt(np.sum(cross**2)) / 2


def calculate_temperatures(mesh: Mesh, config: Config, y0: ndarray, t: ndarray) -> ndarray:
    """Calculates temperatures of mesh elements.

    Args:
        mesh (Mesh): model.
        config (Config): config.
        y0 (ndarray): boundary condition.
        t (ndarray): time interval.

    Returns:
        (time range, [mesh part1 temperature, ...])
    """
    
    # Solve ODE
    return integrate.odeint(EquationEvaluator(mesh, config).eval_equation, y0, t)