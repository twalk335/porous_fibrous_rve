# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 09:50:37 2023

@author: kutsj
"""
import numpy as np
import pyvtk

from mono_fiber import cylinder_maker
from scipy.spatial.distance import cdist

# class Fiber:
#     def __init__(self, center, radius):
#         self.x = center[0]
#         self.

# class Circle:
#     def __init__(self, center, radius):
#         self.center = center
#         self.radius = radius
    
#     def move(self, dx, dy):
#         self.center[0] += dx
#         self.center[1] += dy
    

    
# def intersected(cir_1, cir_2):
#     return np.norm(cir_1.center - cir_2.center) < np.abs(cir_1.radius + cir_2.radius)

# def push_off(cir_1, cir_2):
    

def merge_meshes(*meshes):
    
    # create arrays of points and cells using generators 
    gp = [np.array(mesh.points) for mesh in meshes]
    
    # cells contain links to points by its number. Since we concatenated points, numbers of second 
    # (and every following one) will be increased by cumulative sum of body points number
    body_points_num = np.array([len(mesh.points) for mesh in meshes])
    
    ge = [np.array(meshes[i].elements) + np.sum(body_points_num[:i]) for i in range(len(meshes))]
    bodies_cells = np.cumsum(len(mesh.elements) for mesh in meshes)
    # concatination of points and cells; 
    global_points = np.vstack(gp)
    global_cells = np.vstack(ge)
    
    
    return (global_points, global_cells, bodies_cells)



def main():
    
    f_num = 100
    f_diam = 2


    cL = 100; cW = 100; cH = 20;


    # seed = 100
    f_centers = np.random.default_rng(100).uniform(- (cL - f_diam) / 2, (cL - f_diam) / 2, [f_num,2])
    radiuses = np.expand_dims(np.ones(f_num)*1.3, axis=1)

    distances = cdist(f_centers, f_centers, metric = "euclidean")
    buf = cdist(radiuses, -radiuses, metric='minkowski', p=1.)

    res = np.tril(distances < buf, -1)
    initial = np.tril(distances < buf, -1)

    ij = np.argwhere(res)

    for k in range(1000):
        
        
        if np.any(res):
            
            for i,j in ij:
                p1 = f_centers[i, :]
                # y1 = f_centers[i, 1]
                
                p2 = f_centers[j, :]
                # y2 = f_centers[j, 1]
                
                dx = buf[i,j] * (p1[0] - p2[0]) / np.linalg.norm(p1 - p2)
                dy = buf[i,j] * (p1[1] - p2[1]) / np.linalg.norm(p1 - p2)
                
                f_centers[i,0] += dx/2
                f_centers[i,1] += dy/2
                
                f_centers[j,0] -= dx/2
                f_centers[j,1] -= dy/2
                
                if 
        else:
            print(k)
            break
        
        distances = cdist(f_centers, f_centers, metric = "euclidean")
        res = np.tril(distances < buf, -1)

    distances2 = cdist(f_centers, f_centers, metric = "euclidean")
    res2 = np.tril(distances2 < buf, -1)
    
    fibers = [cylinder_maker(10, cW, f_diam/2, (f_centers[i,0], f_centers[i,1], -cH)) for i in range(f_num)]
    
    points, cells, bodies = merge_meshes(*fibers)    
    
    
    vtkelements = pyvtk.VtkData(
        pyvtk.UnstructuredGrid(
            points,
            tetra = cells),
                "Mesh")
    vtkelements.tofile("rve2")
    
if __name__=="__main__":
    main()

