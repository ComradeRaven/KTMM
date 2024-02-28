###########
# IMPORTS #
###########


# Math
import math
# Handy arrays
import numpy as np

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