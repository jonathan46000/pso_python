#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   '.src/circular_patch/func_F.py'
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
    ## substrate information
    h = 1.6  # standard thickness of FR4
    epsilon_r = 4.4  # dielectric constant, standard permittivity of FR4
    
    try:
        radius = X[0]  # radius of circular patch in mm
        
        # convert dimensions from mm to m
        radius_m = radius / 1000
        h_m = h / 1000
        
        # For a circular patch antenna, the formula uses the Bessel function
        # But we can use the empirical formula with fringing effect
        
        # Calculate the effective radius to account for fringing fields
        # Formula: a_eff = a * sqrt(1 + (2*h/(pi*epsilon_r*a)) * (ln(pi*a/(2*h)) + 1.7726))
        # where a is the physical radius
        
        # Simplified formula that accounts for fringing
        a_eff = radius_m * (1 + (2*h_m)/(np.pi*epsilon_r*radius_m) * (np.log(np.pi*radius_m/(2*h_m)) + 1.7726))**0.5
        
        # Calculate the resonant frequency using the dominant TM11 mode
        # For TM11 mode, the formula is f = (c * 1.8412)/(2 * pi * a_eff * sqrt(epsilon_r))
        # where 1.8412 is the first zero of the derivative of the Bessel function of first kind and first order
        
        # Calculate resonant frequency (in Hz)
        F[0] = (c * 1.8412) / (2 * np.pi * a_eff * np.sqrt(epsilon_r)) #/ 1e9
        
    except:
        noErrors = False
    
    return F, noErrors
