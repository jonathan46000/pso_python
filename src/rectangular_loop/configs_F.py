#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   '.src/rectangular_loop/configs_F.py'
#   Constant values for objective function. Formatted for
#       automating objective function integration
#
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: May 25, 2024
##--------------------------------------------------------------------\
import sys
try: # for outside func calls
    sys.path.insert(0, './pso_python/src/')
    from rectangular_loop.func_F import func_F
    from rectangular_loop.constr_F import constr_F
except: # for local
    from func_F import func_F
    from constr_F import constr_F

OBJECTIVE_FUNC = func_F
CONSTR_FUNC = constr_F
OBJECTIVE_FUNC_NAME = "rectangular_loop.func_F"
CONSTR_FUNC_NAME = "rectangular_loop.constr_F"

# problem dependent variables
## variables are [LENGTH_X, LENGTH_Y, WIRE RAD] in mm
## lower is bounded to 5mm, upper is bounded to create a large search area
## because this is a real-world based model, bounds need to reflect the selected target

LB = [[5, 5, 0.1]]           # Lower boundaries for input
UB = [[1e3,1e3,5]]         # Upper boundaries for input


IN_VARS = 3                 # Number of input variables (x-values)
OUT_VARS = 1                # Number of output variables (y-values)

## default target is 2.4 GHz
TARGETS = [2.4e9]           # Target values for output
GLOBAL_MIN = None           # Global minima, if they exist