###########
# IMPORTS #
###########


# Math
import math
# Handy arrays
import numpy as np
# Custom modules
import lib.utils as utils

# For annotations
from numpy import ndarray
from io import TextIOWrapper


######################
# Container for mesh #
######################


class MeshPart:
    
    def __init__(self, faces: ndarray) -> None:
        self.faces = faces
    
    
    def calculate_area(self, vertices) -> None:
        self.area = 0
        for face in self.faces:
            self.area += utils.triangle_area(vertices[face])


class Mesh:
    
    def __init__(self, filepath: str) -> None:
        # Load data
        self.vertices, self.mesh_parts = self.load_mesh(filepath)
        
        # Calculate area for mesh parts
        for mesh in self.mesh_parts:
            mesh.calculate_area(self.vertices)
    
    
    def load_mesh(self, filepath: str) -> tuple[ndarray, list[MeshPart]]:
        # Geometry
        vertices = []
        mesh_parts = []
        
        # Open file
        with open(filepath, 'r') as f:
            faces = []
            new_mesh_part_token = False
            
            line = f.readline()
            while line:
                # Get line token
                firstSpace = line.find(' ')
                token = line[0:firstSpace]
                
                if token == 'v':
                    # Save vertex
                    vertices.append([float(x) for x in line.replace('v  ', '').replace('\n', '').split(' ')])
                
                elif token == 'f':
                    # Save face (respect vertex indexing starting at 0, not 1)
                    faces.append([int(v)-1 for v in line.replace('f ', '').replace(' \n', '').split(' ')])
                
                elif token == 'g':
                    # New mesh part was found
                    new_mesh_part_token = True
                
                elif token == '#':
                    if new_mesh_part_token:
                        # Add new object part
                        mesh_parts.append(MeshPart(np.array(faces)))
                        # Clear faces list
                        faces = []
                        
                        new_mesh_part_token = False
                
                # Next line
                line = f.readline()
        
        return np.array(vertices), mesh_parts