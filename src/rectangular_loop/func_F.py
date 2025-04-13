#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   '.src/rectangular_loop/func_F.py'
#   Function for objective function evaluation.
#   This objective function REQUIRES A SPECIFIC ORDER OF INPUTS   
#
#
#   Author(s): Lauren Linkous
#   Last update: April 13, 2025
##-------------------------------------------------------------------------------\

import numpy as np

def func_F(X, NO_OF_OUTS=1):
    F = np.zeros((NO_OF_OUTS))
    noErrors = True
    
    # constants
    ## speed of light in m/s
    c = 3e8
    
    try:
        # Rectangular loop dimensions
        length_x = X[0]  # length in x direction in mm
        length_y = X[1]  # length in y direction in mm
        wire_radius = X[2]  # radius of the wire in mm
        
        # convert dimensions from mm to m
        length_x_m = length_x / 1000
        length_y_m = length_y / 1000
        wire_radius_m = wire_radius / 1000
        
        # Calculate perimeter
        perimeter_m = 2 * (length_x_m + length_y_m)
        
        # Effective radius for equivalent circular loop
        effective_radius_m = perimeter_m / (2 * np.pi)
        
        # Correction factor based on wire thickness
        thickness_ratio = wire_radius_m / effective_radius_m
        correction = 1.0 - (0.2 * np.log10(1 + 10 * thickness_ratio))
        
        # Calculate resonant frequency with correction (in Hz)
        F[0] = (c * correction) / perimeter_m
            
    except:
        noErrors = False
    
    return F, noErrors
