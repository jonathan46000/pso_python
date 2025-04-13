#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   '.src/loop_antenna/func_F.py'
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
        # For circular loop
        if len(X) == 1:
            # Only circumference provided (circular loop assumed)
            circumference = X[0]  # circumference of loop in mm
            
            # convert dimensions from mm to m
            circumference_m = circumference / 1000
            
            # For a loop antenna, resonance occurs when circumference ≈ wavelength
            # Formula: circumference = λ
            # Therefore: f = c / λ = c / circumference
            
            # Calculate resonant frequency (in Hz)
            F[0] = c / circumference_m 


        elif len(X) == 2:
            # Radius and wire radius provided (circular loop)
            radius = X[0]  # radius of loop in mm
            wire_radius = X[1]  # radius of the wire in mm
            
            # convert dimensions from mm to m
            radius_m = radius / 1000
            wire_radius_m = wire_radius / 1000
            
            # Calculate circumference
            circumference_m = 2 * np.pi * radius_m
            
            # Correction factor based on wire thickness
            # For thicker wires relative to loop size, resonant length decreases
            thickness_ratio = wire_radius_m / radius_m
            correction = 1.0 - (0.2 * np.log10(1 + 10 * thickness_ratio))
            
            # Calculate resonant frequency with correction (in Hz)
            F[0] = (c * correction) / circumference_m 

              
           
    except:
        noErrors = False
    
    return F, noErrors