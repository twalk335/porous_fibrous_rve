# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 09:50:37 2023

@author: kutsj
"""
import numpy as np
import pyvtk

from mono_fiber import cylinder_maker


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
    f_centers_x = np.random.default_rng(100).uniform(- (cL - f_diam) / 2, (cL - f_diam) / 2, f_num)
    f_centers_y = np.random.default_rng(101).uniform(- (cH - f_diam) / 2, (cH - f_diam) / 2, f_num)
    
    fibers = [cylinder_maker(10, cW, f_diam/2, (f_centers_x[i], f_centers_y[i], -cH)) for i in range(f_num)]
    
    points, cells, bodies = merge_meshes(*fibers)    
    
    
    vtkelements = pyvtk.VtkData(
        pyvtk.UnstructuredGrid(
            points,
            tetra = cells),
                "Mesh")
    vtkelements.tofile("rve")
    
if __name__=="__main__":
    main()

