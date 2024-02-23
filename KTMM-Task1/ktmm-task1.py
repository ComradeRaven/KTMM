import numpy as np
import lib.utils as Utils
from lib.classes.mesh import Mesh


filepath = 'model/model1.obj'

mesh = Mesh(filepath)
print('vertex array shape: ', mesh.vertices.shape)

# Intersection between parts from bottom to top (from part[0] to part [4]) are located at
# y = 0, 6, 8, 9 respectively
intersection_y = [0, 6, 8, 9]
intersection_areas = np.empty((len(mesh.mesh_parts) - 1))
for i in range(0, 4):
    mesh_part = mesh.mesh_parts[i]
    intersection_area = 0
    
    for face in mesh_part.faces:
        vert = mesh.vertices[face]
        
        # Check Y coordinates
        if vert[0][1] == vert[1][1] == vert[2][1] == intersection_y[i]:
            intersection_area += Utils.triangle_area(mesh.vertices[face])
    
    intersection_areas[i] = intersection_area

print('Intersection areas:')
for intersection_area in intersection_areas:
    print(intersection_area)

# Substract intersection from mesh parts
mesh.mesh_parts[0].area -= intersection_areas[0]
mesh.mesh_parts[1].area -= intersection_areas[0] + intersection_areas[1]
mesh.mesh_parts[2].area -= intersection_areas[1] + intersection_areas[2]
mesh.mesh_parts[3].area -= intersection_areas[2] + intersection_areas[3]
mesh.mesh_parts[4].area -= intersection_areas[3]

print('Mesh parts areas:')
for mesh in mesh.mesh_parts:
    print(mesh.area)