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


diam = 0.2


gmsh.initialize()

gmsh.model.add("fibers_test")

seed = 100

RG = np.random.default_rng(seed)

width = 2
height = 2
depth = 2
diam = 0.05

x_min = -width/2
x_max = width/2

y_min = -height/2
y_max = height/2

z_min = -depth/2
z_max = depth/2

fibers_num = 100

xy = RG.uniform(-1, 1, [fibers_num, 2]) @ np.array([[width/2,0],[0, height/2]])
alpha = RG.uniform(0, 2*np.pi, [fibers_num,1])
beta = np.pi/2 - halfnorm.rvs(size = [fibers_num, 1]) * 20 * np.pi / 180


for i in range(fibers_num):
    sf.generate_fiber_by_angles(xy[i,:], alpha[i,0], beta[i,0], [z_min, z_max], diam)
    
gmsh.model.occ.synchronize()
gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 7)
# gmsh.option.setNumber("Mesh.RandomFactor", 20)
gmsh.model.mesh.generate(3)

gmsh.write("fibers.vtk")

gmsh.finalize()