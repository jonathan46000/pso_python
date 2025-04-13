#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   '.src/rectangular_patch/func_F.py'
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
    epsilon_r = 4.4 # dielectric constant. standard permitivity of FR4


    try:

        length =  X[0]  # length in mm 
        width = X[1]    # width in mm

        # convert dimensions from mm to m
        length = length / 1000
        width = width / 1000
        h = h / 1000

        # calculate effective dielectric constant
        epsilon_eff = ((epsilon_r + 1) / 2) + ((epsilon_r - 1) / 2) * (1 + 12 * h / width) ** (-0.5)
        
        # calculate extension length
        delta_L = 0.412 * h * ((epsilon_eff + 0.3) * (width / h + 0.264)) / ((epsilon_eff - 0.258) * (width / h + 0.8))
        
        # calculate effective length
        L_eff = length + 2 * delta_L
        
        # calculate resonant frequency (in Hz)
        F[0] = c / (2 * L_eff * (epsilon_eff ** 0.5)) #/ 1e9

    except:
        noErrors = False
    
    return F, noErrors