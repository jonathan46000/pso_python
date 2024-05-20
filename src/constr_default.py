#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   './src/pso_basic/constr_default.py'
#   Function for default constraints. Called if user does not pass in 
#       constraints for objective function or problem being optimized. 
#
#   Author(s): Jonathan Lundquist, Lauren Linkous
#   Last update: May 20, 2024
##--------------------------------------------------------------------\


import numpy as np

def constr_default(x):
    return True
