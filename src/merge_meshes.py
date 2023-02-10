from meshpy.tet import MeshInfo, build
from math import sin, cos, pi, sqrt
import numpy as np
import pyvtk
import random
from Cylinder import cylinder_maker


def merge_meshes(*meshes):

    # create arrays of points and cells using generators
    gp = [np.array(mesh.points) for mesh in meshes]

    # cells contain links to points by its number. Since we concatenated points, numbers of second
    # (and every following one) will be increased by cumulative sum of body points number
    body_points_num = np.array([len(mesh.points) for mesh in meshes])

    ge = [np.array(meshes[i].elements) + np.sum(body_points_num[:i]) for i in range(len(meshes))]
    bodies_cells = np.cumsum(len(mesh.elements) for mesh in meshes)
    # concatenation of points and cells;
    global_points = np.vstack(gp)
    global_cells = np.vstack(ge)

    return global_points, global_cells, bodies_cells
