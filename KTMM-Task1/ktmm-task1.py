import lib.utils as Utils
from lib.classes.mesh import Mesh

filepath = 'model/model1.obj'

mesh = Mesh(filepath)

print(mesh.vertices.shape)
i = [1, 8, 7]
print(mesh.vertices[i])
print(Utils.triangle_area(mesh.vertices[i]))
print(mesh.mesh_parts[0].area)