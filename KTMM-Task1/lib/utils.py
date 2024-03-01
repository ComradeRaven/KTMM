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


def eval_equation(y, t, mesh: Mesh, config: Config) -> ndarray:
    """Evaluates task equation.

    Args:
        y (_type_): y vector.
        t (_type_): time point.
        mesh (Mesh): model.
        config (Config): config.

    Returns:
        New y vector.
    """
    
    # Q_TC
    q_tc = - mesh.intercestions_surfaces * config.therm_cond_coefs
    for i in range(q_tc.shape[0]):
        for j in range(i+1, q_tc.shape[1]):
            q_tc *= y[j] - y[i]
    
    # Q_E
    q_e = - 5.67 * config.eps * mesh.surfaces * (y/100)**4
    
    # Q_R
    q_r = eval(config.q_r, globals(), locals())
    
    # Formula from docs
    return (np.sum(q_tc, axis=1) + q_e + q_r) / config.c


def calculate_temperatures(mesh: Mesh, config: Config) -> tuple[ndarray, list[ndarray]]:
    """Calculates temperatures of mesh elements.

    Args:
        mesh (Mesh): model.
        config (Config): config.

    Returns:
        (time range, [mesh part1 temperature, ...])
    """
    
    # Wrap evaluation function
    eval_equation_wrapping = lambda y, t: eval_equation(y, t, mesh, config)
    
    # Solve ODE
    t = eval(config.t, globals(), locals())
    values = integrate.odeint(eval_equation_wrapping, config.y0, t)
    
    # Extract functions values
    y1 = values[:, 0]
    y2 = values[:, 1]
    y3 = values[:, 2]
    y4 = values[:, 3]
    y5 = values[:, 4]
    
    # Construct result
    return t, [y1, y2, y3, y4, y5]