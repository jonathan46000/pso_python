#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   '.src/loop_antenna/configs_F.py'
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
    from loop_antenna.func_F import func_F
    from loop_antenna.constr_F import constr_F
except: # for local
    from func_F import func_F
    from constr_F import constr_F

OBJECTIVE_FUNC = func_F
CONSTR_FUNC = constr_F
OBJECTIVE_FUNC_NAME = "loop_antenna.func_F"
CONSTR_FUNC_NAME = "loop_antenna.constr_F"

# problem dependent variables
## variables are [...] in mm
## lower is bounded to 5mm, upper is bounded to create a large search area
## because this is a real-world based model, bounds need to reflect the selected target

# CIRCUMFERENCE ONLY
LB = [[10]]           # Lower boundaries for input
UB = [[1e5]]         # Upper boundaries for input
## problem dimensions
IN_VARS = 1                 # Number of input variables (x-values)
OUT_VARS = 1                # Number of output variables (y-values)

# # LOOP RADIUS and WIRE RADIUS
# LB = [[2, 0.01]]        # Lower boundaries for input
# UB = [[1e3, 5]]         # Upper boundaries for input
# ## problem dimensions
# IN_VARS = 2                 # Number of input variables (x-values)
# OUT_VARS = 1                # Number of output variables (y-values)

## default target is 2.4 GHz
TARGETS = [2.4e9]           # Target values for output
GLOBAL_MIN = None           # Global minima, if they exist

