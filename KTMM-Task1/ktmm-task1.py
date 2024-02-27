###########
# IMPORTS #
###########


# Handy arrays
import numpy as np
# Custom modules
import lib.utils as Utils
from lib.classes.mesh import Mesh


###########
# Program #
###########

filepath = 'model/model1.obj'

mesh = Mesh(filepath)

print('vertex array shape: ', mesh.vertices.shape)
print('Mesh parts surfaces:')
print(mesh.surfaces)
print('Intersections surfaces:')
print(mesh.intercestions_surfaces)