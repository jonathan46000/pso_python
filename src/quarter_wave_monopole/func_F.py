#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   '.src/quarter_wave_monopole/func_F.py'
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
    ## correction factor for monopole antennas
    k = 0.95  # velocity factor (typically 0.93-0.97 for thin wire monopoles)
    
    try:
        length = X[0]  # length of monopole in mm
        
        # optional parameters if provided
        if len(X) > 1:
            wire_diameter = X[1]  # wire diameter in mm
            # adjust k based on wire diameter to length ratio
            # for thicker wires, the velocity factor decreases
            # (simplified approximation)
            diameter_to_length_ratio = wire_diameter / length
            if diameter_to_length_ratio > 0.01:
                k = 0.95 - (diameter_to_length_ratio * 2)
                k = max(0.90, k)  # ensure k doesn't get too small
        
        # convert dimensions from mm to m
        length_m = length / 1000
        
        # For a monopole, the resonant length is a quarter wavelength (of the frequency)
        # formula: length = λ/4 * k
        # rearranged: λ = 4 * length / k
        # then: f = c / λ = c / (4 * length / k)
        
        # calculate resonant frequency (in Hz)
        F[0] = (c * k) / (4 * length_m) 

    except:
        noErrors = False
    
    return F, noErrors