# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 21:43:49 2023

@author: MKuts
"""

import gmsh
import numpy as np
from numpy.linalg import norm

from scipy.stats import halfnorm

import SpatialFiber as sf





gmsh.initialize()

gmsh.model.add("fibers_test")

seed = 100

RG = np.random.default_rng(seed)

width = 2
height = 2
depth = 2
diam = 0.1

x_min = -width/2
x_max = width/2

y_min = -height/2
y_max = height/2

z_min = -depth/2
z_max = depth/2

fibers_num = 50

xy = RG.uniform(-1, 1, [fibers_num, 2]) @ np.array([[width/2,0],[0, height/2]])
alpha = RG.uniform(0, 2*np.pi, [fibers_num,1])
beta = np.pi/2 - halfnorm.rvs(size = [fibers_num, 1]) * 20 * np.pi / 180

fibers = []
fibers_keys = {}

for i in range(fibers_num):
    fibers.append(sf.generate_fiber_by_angles(xy[i,:], alpha[i,0], beta[i,0], [z_min, z_max], diam))
    fibers_keys[i+1] = [fibers[-1]]

latest_index = len(fibers)
gmsh.model.occ.synchronize()
for i in range(fibers_num):
    
    for j in range(i+1,fibers_num):
        dist, t_a, t_b = sf.sk_min_dist(fibers[i], fibers[j])
        if dist < 0.95*diam:
            gmsh.model.occ.synchronize()
            print("intersected (",i,",",j,")",)
            latest_index += 1
            f1a = fibers[i].start_point
            f1b = fibers[i].end_point
            f2a = fibers[j].start_point
            f2b = fibers[j].end_point
            print("(",fibers[i].body_ind,",",fibers[j].body_ind,")")
            buf_ind = gmsh.model.occ.fuse([(3,fibers[i].body_ind)], [(3, fibers[j].body_ind)], latest_index)
            print("new index = ", latest_index)
            fibers_keys[latest_index] = fibers_keys[fibers[i].body_ind] + fibers_keys[fibers[j].body_ind]
            print(fibers_keys[latest_index])
            fibers_keys[fibers[i].body_ind] = []
            fibers_keys[fibers[j].body_ind] = []
            for fiber in fibers_keys[latest_index]:
                fiber.body_ind = latest_index

            
# cutters = []

# cutters.append(gmsh.model.occ.addBox(2*x_min, 2*y_min, 2*z_min, width/2, 2*height, 2*depth))
# cutters.append(gmsh.model.occ.addBox(x_max, 2*y_min, 2*z_min, width/2, 2*height, 2*depth))
# cutters.append(gmsh.model.occ.addBox(2*x_min, 2*y_min, 2*z_min, 2*width, 2*height, depth/2))
# cutters.append(gmsh.model.occ.copy())     
gmsh.model.occ.synchronize()
gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 8)
# gmsh.option.setNumber("Mesh.RandomFactor", 20)
gmsh.model.mesh.generate(3)

gmsh.write("fibers.vtk")

gmsh.finalize()