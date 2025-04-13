#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   '.src/circular_patch/configs_F.py'
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
    from circular_patch.func_F import func_F
    from circular_patch.constr_F import constr_F
except: # for local
    from func_F import func_F
    from constr_F import constr_F

OBJECTIVE_FUNC = func_F
CONSTR_FUNC = constr_F
OBJECTIVE_FUNC_NAME = "circular_patch.func_F"
CONSTR_FUNC_NAME = "circular_patch.constr_F"

# problem dependent variables
## variables are [LENGTH, WIDTH] in mm
## lower is bounded to 2mm, upper is bounded to create a large search area
## because this is a real-world based model, bounds need to reflect the selected target
LB = [[2]]           # Lower boundaries for input
UB = [[50]]          # Upper boundaries for input

## problem dimensions
IN_VARS = 1                 # Number of input variables (x-values)
OUT_VARS = 1                # Number of output variables (y-values)

## default target is 2.4 GHz
TARGETS = [2.4e9]           # Target values for output
GLOBAL_MIN = None           # Global minima, if they exist