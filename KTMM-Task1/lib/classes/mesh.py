###########
# IMPORTS #
###########


# Handy arrays
import numpy as np
# Custom modules
import lib.utils as utils

# For annotations
from numpy import ndarray


######################
# Container for mesh #
######################


class MeshPart:
    '''Holds faces, associated with some mesh part.'''
    
    def __init__(self, faces: ndarray) -> None:
        self.faces = faces
    
    
    def calculate_surface(self, vertices: ndarray, intercestions_surface: ndarray) -> float:
        '''Calculates mesh part surface (without intersections).'''
        
        # Total surface
        surface = 0
        for face in self.faces:
            surface += utils.triangle_surface(vertices[face])
        
        # Substract intersections
        surface -= intercestions_surface
        
        return surface


class Mesh:
    '''Represents .obj mesh.'''
    
    def __init__(self, filepath: str) -> None:
        # Load data
        self.vertices, self.mesh_parts = self.load_mesh(filepath)
        
        # Intersections matrix
        self.intercestions_surfaces = utils.intercestions_matrix(self)
        
        # Calculate surface for each mesh part
        self.surfaces = []
        for i in range(len(self.mesh_parts)):
            self.surfaces.append(self.mesh_parts[i].calculate_surface(self.vertices, np.sum(self.intercestions_surfaces[i])))
        self.surfaces = np.array(self.surfaces)
    
    
    def load_mesh(self, filepath: str) -> tuple[ndarray, list[MeshPart]]:
        '''Loads mesh geometry.'''
        
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