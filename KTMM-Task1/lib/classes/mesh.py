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
    """Holds faces, associated with some mesh part.
    """
    
    def __init__(self, faces: ndarray) -> None:
        self.faces = faces
    
    
    def calculate_surface(self, vertices: ndarray, intersections_surface: ndarray) -> float:
        """Calculates mesh part surface.

        Args:
            vertices (ndarray): vertices of entire mesh.
            intersections_surface (ndarray): mesh part intersections (with other parts) surface.

        Returns:
            float: mesh part surface.
        """
        
        # Total surface
        surface = 0
        for face in self.faces:
            surface += utils.triangle_surface(vertices[face])
        
        # Substract intersections
        surface -= intersections_surface
        
        return surface


class Mesh:
    """Represents .obj mesh.
    """
    
    def __init__(self, filepath: str) -> None:
        # Load data
        self.vertices, self.mesh_parts = self.load_mesh(filepath)
        
        # Intersections matrix
        self.intercestions_surfaces = self.intercestions_matrix()
        
        # Calculate surface for each mesh part
        self.surfaces = []
        for i in range(len(self.mesh_parts)):
            self.surfaces.append(self.mesh_parts[i].calculate_surface(self.vertices, np.sum(self.intercestions_surfaces[i])))
        self.surfaces = np.array(self.surfaces)
    
    
    def load_mesh(self, filepath: str) -> tuple[ndarray, list[MeshPart]]:
        """Loads mesh geometry.

        Args:
            filepath (str): path to file.

        Returns:
            tuple[ndarray, list[MeshPart]]: vertices and list of mesh parts.
        """
        
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
    
    
    def intercestions_matrix(self) -> ndarray:
        """Produces matrix with intersections surfaces.

        Returns:
            ndarray: matrix with intersections surfaces.
        """
        
        # Intersection between parts from bottom to top (from part[0] to part [4]) are located at
        # y = 0, 6, 8, 9 respectively
        intersections_y = [0, 6, 8, 9]
        intersection_surfaces = np.empty((len(self.mesh_parts) - 1))
        for i in range(0, 4):
            mesh_part = self.mesh_parts[i]
            intersection_surface = 0
            
            for face in mesh_part.faces:
                vert = self.vertices[face]
                
                # Check Y coordinates
                if vert[0][1] == vert[1][1] == vert[2][1] == intersections_y[i]:
                    intersection_surface += utils.triangle_surface(self.vertices[face])
            
            intersection_surfaces[i] = intersection_surface
        
        # Intersections surfaces matrix filling
        intersections_surfaces = np.zeros((5, 5))
        intersections_surfaces[0, 1] = intersection_surfaces[0]
        intersections_surfaces[1, 2] = intersection_surfaces[1]
        intersections_surfaces[2, 3] = intersection_surfaces[2]
        intersections_surfaces[3, 4] = intersection_surfaces[3]
        
        return intersections_surfaces