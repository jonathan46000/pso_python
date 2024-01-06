#! /usr/bin/python3
import numpy as np


def constr_E_const_Lg_Wg_h(x):
    if (x[2] <= x[1]) and \
        (x[3] >= (x[4]/2)) and \
            ((x[3] + x[4]/2) <= (x[5]/2)) and\
                (np.abs(x[0]) <= (x[1]/2)):
        F = True
    else:
        F = False

    return F