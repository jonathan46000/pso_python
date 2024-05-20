#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   './pso_basic/src/func_F.py'
#   Function for objective function evaluation.
#   Has checks for floating point error, but these should never trigger
#       if constraints have been properly applied.
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: May 20, 2024
##--------------------------------------------------------------------\

import numpy as np
np.seterr(all='raise') # explicitly raise the FloatingPointError as an error


def func_F(x):
    NO_OF_OUTS = 2
    F = np.zeros((NO_OF_OUTS, 1))
   
    try:
        F[0] = (x[0]-0.5) ** 2 + (x[1]-0.1) ** 2
    except FloatingPointError as err:
        print(err)
        print("x[0] value in '(x[0]-0.5) ** 2 + (x[1]-0.1) ** 2' that caused error: " + str(x[0]))
        print("x[1] value in '(x[0]-0.5) ** 2 + (x[1]-0.1) ** 2' that caused error: " + str(x[1]))
        print(".........................................................................")

    try:
        F[1] = (x[2]-0.2) ** 4
    except FloatingPointError as err:
        print(err)
        print("x[2] value in '(x[2]-0.2) ** 4' that caused error: " + str(x[2]))
        print(".........................................................................")
        
    return F
