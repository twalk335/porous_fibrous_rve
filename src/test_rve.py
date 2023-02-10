# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 09:50:37 2023

@author: kutsj
"""
import numpy as np
import pyvtk

from MeshpyRVE import fibrous_system

def main():
    
    fibrous_system(100, 1, 10, 0, 50, 0)

    
if __name__=="__main__":
    main()

