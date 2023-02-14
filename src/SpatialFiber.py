# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 13:00:09 2023

@author: MKuts
"""
import gmsh

import numpy as np
import scipy as sc


from numpy.linalg import norm

class Str8Fiber:
    def __init__(self, p1, p2, d):
        self.start_point = np.array(p1)
        self.end_point = np.array(p2)
        self.d = d
        
        p = self.start_point
        e = self.end_point - p
        
        self.body_ind = gmsh.model.occ.addCylinder(*p, *e, d/2)
        
    def __getitem__(self, key):
        if key == "x0":
            return self.start_point[0]
        elif key =="y0":
            return self.start_point[1]
        elif key == "z0":
            return self.start_point[2]
        elif key == "dx":
            return self.end_point[0] - self.start_point[0]
        elif key == "dy":
            return self.end_point[1] - self.start_point[1]
        elif key == "dz":
            return self.end_point[2] - self.start_point[2]
        elif key == "p":
            return self.start_point
        elif key == "e":
            return self.end_point - self.start_point
        
    def get_point(self, t):
        return self["p"] + self["e"]*t        
   
def dist(t, fib0, fib1):
    x_l0 = fib0["x0"] - t[0]*fib0["dx"]
    y_l0 = fib0["y0"] - t[0]*fib0["dy"]
    z_l0 = fib0["z0"] - t[0]*fib0["dz"]
    
    x_l1 = fib1["x0"] - t[0]*fib1["dx"]
    y_l1 = fib1["y0"] - t[0]*fib1["dy"]
    z_l1 = fib1["z0"] - t[0]*fib1["dz"]

    return np.sqrt((x_l0 - x_l1)**2 + (y_l0 - y_l1)**2 + (z_l0 - z_l1)**2)

def sk_min_dist(fib_a, fib_b):
    
    n = np.cross(fib_a["e"], fib_b["e"])
    d = np.abs(np.dot(n, fib_a["p"] - fib_b["p"]))/np.linalg.norm(n, 2)
    t0 = np.dot(np.cross(fib_b["e"], n), fib_b["p"] - fib_a["p"])/np.dot(n,n)
    t1 = np.dot(np.cross(fib_a["e"], n), fib_b["p"] - fib_a["p"])/np.dot(n,n)
    return d, t0, t1
    
def parallel(fib_a, fib_b, eps_ = 1e-5):
    return norm(np.cross(fib_a["e"], fib_b["e"]))/(norm(fib_a["e"])*norm(fib_b["e"])) < eps_

def check_sk_intersection(fib_a, fib_b):
    dist, t_a, t_b = sk_min_dist(fib_a, fib_b)
    
    if dist < (fib_a.d+fib_b.d)/2:
        return True, dist, t_a, t_b
    else:
        return False, dist, t_a, t_b
        
    
def add_fiber_cylinder(fiber, ii = -1):
    return gmsh.model.occ.addCylinder(*fiber["p"], *fiber["e"], fiber.d/2, ii)


def calc_box(point, diam):
    xmin = point[0] - diam
    xmax = point[0] + diam
    
    ymin = point[1] - diam
    ymax = point[1] + diam
    
    zmin = point[2] - diam
    zmax = point[2] + diam
    
    return np.array([xmin, ymin, zmin, xmax, ymax, zmax])


def generate_fiber_by_angles(xy, alpha, beta, z_bounds, diam):
    new_beta = np.arctan(np.tan(beta)/np.abs(np.cos(alpha)))
    phi = alpha
    theta = np.pi/2 - new_beta
    
    dz = (z_bounds[1] - z_bounds[0])/2 + diam/2;
    
    # r = dz / np.cos(theta);
    dx = dz*np.tan(theta)*np.cos(phi)
    dy = dz*np.tan(theta)*np.sin(phi)
    
    pA = [xy[0] - dx, xy[1] - dy, z_bounds[0] - diam/2]
    pB = [xy[0] + dx, xy[1] + dy, z_bounds[1] + diam/2]
    
    return Str8Fiber(pA, pB, diam)


    
    

# import matplotlib.pyplot as plt

# plt.hist(theta)    






        