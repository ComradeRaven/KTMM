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


def calculate_temperatures(mesh: Mesh, config: Config) -> tuple[ndarray, list[ndarray]]:
    """Calculates temperatures of mesh elements.

    Args:
        mesh (Mesh): model.
        config (Config): config.

    Returns:
        (time range, [mesh part1 temperature, ...])
    """
    
    # Equation evaluator
    eq_eval = EquationEvaluator(mesh, config)
    
    # Solve ODE
    t = eval(config.t, globals(), locals())
    odeinit_output = integrate.odeint(eq_eval.eval_equation, config.y0, t)
    
    # Extract functions values
    y1 = odeinit_output[:, 0]
    y2 = odeinit_output[:, 1]
    y3 = odeinit_output[:, 2]
    y4 = odeinit_output[:, 3]
    y5 = odeinit_output[:, 4]
    
    # Construct result
    return t, [y1, y2, y3, y4, y5], odeinit_output