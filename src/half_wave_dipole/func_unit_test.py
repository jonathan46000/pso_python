#! /usr/bin/python3
##--------------------------------------------------------------------\
#   pso_basic
#   '.src/half_wave_dipole/func_unit_test.py'
#   Unit test for the half wave dipole antenna objective function.
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
    ## correction factor for dipole antennas
    k = 0.97  # velocity factor (typically 0.93-0.97 for wire dipoles)
    
    try:
        total_length = X[0]  # total length of dipole in mm (both arms combined)
        
        # optional parameters if provided
        if len(X) > 1:
            wire_diameter = X[1]  # wire diameter in mm
            
            # Adjust k based on wire diameter to length ratio
            # For thicker wires, the velocity factor decreases
            # This is a simplified approximation based on empirical data
            diameter_to_length_ratio = wire_diameter / total_length
            if diameter_to_length_ratio > 0.005:
                k = 0.95 - (diameter_to_length_ratio * 3)
                k = max(0.90, k)  # ensure k doesn't get too small
        
        # convert dimensions from mm to m
        length_m = total_length / 1000
        
        # For a dipole, the resonant length is half wavelength
        # Formula: total_length = λ/2 * k
        # Rearranged: λ = 2 * total_length / k
        # Therefore: f = c / λ = c / (2 * total_length / k)
        
        # Calculate resonant frequency (in Hz)
        F[0] = (c * k) / (2 * length_m) 
        
    except:
        noErrors = False
    
    return F, noErrors

# test
total_length = 61 # mm (total length of dipole - both arms)
f, noErr = func_F([total_length])
print(f)

# test with wire diameter specified
total_length = 60  # mm
wire_diameter = 1.5  # mm
f, noErr = func_F([total_length, wire_diameter])
print(f)