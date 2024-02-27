###########
# IMPORTS #
###########


# Math
import math
# Handy arrays
import numpy as np
# Custom modules
from lib.classes.mesh import Mesh

# For annotations
from numpy import ndarray


#########
# Utils #
#########


def triangle_surface(vertices: ndarray) -> float:
    '''Calculates triangle surface in 3D space.'''
    
    # Parallelogram vectors
    vector1 = vertices[1] - vertices[0]
    vector2 = vertices[2] - vertices[0]
    
    # Cross product
    cross = np.cross(vector1, vector2)
    
    # Half of the module of the cross product
    return math.sqrt(np.sum(cross**2)) / 2


def intercestions_matrix(mesh: Mesh) -> ndarray:
    # Intersection between parts from bottom to top (from part[0] to part [4]) are located at
    # y = 0, 6, 8, 9 respectively
    intersections_y = [0, 6, 8, 9]
    intersection_surfaces = np.empty((len(mesh.mesh_parts) - 1))
    for i in range(0, 4):
        mesh_part = mesh.mesh_parts[i]
        intersection_surface = 0
        
        for face in mesh_part.faces:
            vert = mesh.vertices[face]
            
            # Check Y coordinates
            if vert[0][1] == vert[1][1] == vert[2][1] == intersections_y[i]:
                intersection_surface += triangle_surface(mesh.vertices[face])
        
        intersection_surfaces[i] = intersection_surface
    
    # Intersections surfaces matrix filling
    intersections_surfaces = np.zeros((5, 5))
    intersections_surfaces[0, 1] = intersection_surfaces[0]
    intersections_surfaces[1, 0] = intersection_surfaces[0]
    intersections_surfaces[1, 2] = intersection_surfaces[1]
    intersections_surfaces[2, 1] = intersection_surfaces[1]
    intersections_surfaces[2, 3] = intersection_surfaces[2]
    intersections_surfaces[3, 2] = intersection_surfaces[2]
    intersections_surfaces[3, 4] = intersection_surfaces[3]
    intersections_surfaces[4, 3] = intersection_surfaces[3]
    
    return intersections_surfaces
