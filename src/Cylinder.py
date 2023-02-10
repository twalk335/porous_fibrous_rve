from meshpy.tet import MeshInfo, build
from math import sin, cos, pi, sqrt
import numpy as np
import pyvtk
import random


def cylinder_maker(num_points, height, radius, center):
    mesh_info = MeshInfo()
    # We want to approximate a cylinder by creating a coordinate array and a facet array to pass to the build function.
    # To do this, we use polar coordinates to create the bottom and top faces, then connect them with rectangles.
    # num_points = number of vertices in cross-section

    # by default, the cylinder is centered at (0,0,0), but we can translate the center by adding the values we want
    x = center[0]
    y = center[1]
    z = center[2]

    points_array_bottom = np.empty([num_points, 3])  # pre-allocating space for points array
    points_array_top = np.empty([num_points, 3])
    facets_array_middle = np.empty([num_points - 1, 4])  # pre_allocating space for rectangular facets
    top_face = np.linspace(0, num_points - 1, num_points)  # defining the top face
    bottom_face = np.linspace(num_points, num_points * 2 - 1, num_points)  # defining the bottom face

    for i in range(num_points):
        points_array_bottom[i, :] = [x + radius * cos(((2 * pi) / num_points) * i),
                                     y + radius * sin(((2 * pi) / num_points) * i), z]

        points_array_top[i, :] = [x + radius * cos(((2 * pi) / num_points) * i),
                                  y + radius * sin(((2 * pi) / num_points) * i), z + height]

    points_array = np.vstack((points_array_bottom, points_array_top))  # combining the top and bottom faces

    for j in range(num_points - 1):  # populating facet array, the middle part has a predictable rectangle pattern

        facets_array_middle[j, :] = [j, j + num_points, j + num_points + 1, (j + 1)]

    facets_array_middle = np.vstack(
        (facets_array_middle, [0, num_points, 2 * num_points - 1, num_points - 1]))

    # converting arrays to lists to avoid issue of top/bottom and middle faces from having different lengths,
    # then converting the lists of floats to lists of ints, since set_facets requires int lists

    facets_array_middle = (np.ndarray.tolist(facets_array_middle))
    top_face = np.ndarray.tolist(top_face)
    bottom_face = np.ndarray.tolist(bottom_face)
    bottom_face = list(map(int, bottom_face))
    top_face = list(map(int, top_face))
    facets_array_middle = [list(map(int, sublist)) for sublist in facets_array_middle]
    facets_array_middle = [top_face] + [bottom_face] + facets_array_middle

    mesh_info.set_points(points_array)
    mesh_info.set_facets(facets_array_middle)

    mesh = build(mesh_info)
    return mesh
