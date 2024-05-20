#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   './pso_basic/src/constr_F.py'
#   Function for objective function constraints.
#   Has 2 checks: 1 for the function limitations, 1 for float size
#   Returns True if x array passes constraints check, False otherwise   
#
#   Author(s): Jonathan Lundquist, Lauren Linkous
#   Last update: May 20, 2024
##--------------------------------------------------------------------\

import time


def constr_F(x):
    F = True
    # objective function/problem constraints
    if (x[2] > x[0]/2) or (x[2] < 0.1):
        F = False

    # additional cosntraints to deal with an under/overflow issue
    # where the 64 bit floats will not convert to a longfloat(float128) (system issue)
    # The maximum and minimum caps are used here to avoid:
    # 1: an under/overflow issue in the objective function
    # 2: an under/overflow issue in PSO caused by multiplication
    if (x[0]!=0) and ((abs(x[0]) > 5e50) or (abs(x[0]) < 5e-50)):
        F = False
    if (x[1]!=0) and ((abs(x[1]) > 5e50) or (abs(x[1]) < 5e-50)):
        F = False
    if (x[2]!=0) and ((abs(x[2]) > 5e50) or (abs(x[2]) < 5e-50)):
        F = False


    return F