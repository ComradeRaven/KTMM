###########
# IMPORTS #
###########


# Math
import math
# Handy arrays
import numpy as np

# For annotations
from numpy import ndarray


######################
# Container for mesh #
######################


class MeshPart:
    
    def __init__(self, faces: ndarray) -> None:
        self.faces = faces


class Mesh:
    
    def __init__(self, filepath: str) -> None:
        self.mesh_parts = []
        self.vertices = self.load_mesh(filepath, self.mesh_parts)
    
    
    def load_mesh(self, filepath: str, mesh_parts: list[MeshPart]) -> ndarray:
        # Open file
        with open(filepath, 'r') as f:
            # Geometry
            vertices = []
            faces = []
            # Flag
            was_face = True
            
            line = f.readline()
            while line:
                # Get line token
                firstSpace = line.find(' ')
                token = line[0:firstSpace]
                
                if token == 'v':
                    # Update mode
                    if was_face:
                        was_face = False
                        # Add new object part
                        mesh_parts.append(MeshPart(np.array(faces)))
                        # Clear faces list
                        faces = []
                    
                    # Save vertex
                    vertices.append([float(x) for x in line.replace('v  ', '').replace('\n', '').split(' ')])
                elif token == 'f':
                    # Update mode
                    if not was_face:
                        was_face = True
                    
                    # Save face
                    faces.append([int(v) for v in line.replace('f ', '').replace(' \n', '').split(' ')])
                
                # Next line
                line = f.readline()
        
        
        return np.array(vertices)