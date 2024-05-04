#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_python
#   './src/pso_python/function_configs.py'
#   Constant values for objective function. Formatted for
#       automating objective function integration
#
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: May 4, 2024
##--------------------------------------------------------------------\


from func_F import func_F
from constr_F import constr_F


OBJECTIVE_FUNC = func_F
CONSTR_FUNC = constr_F
OBJECTIVE_FUNC_NAME = "pso_python.func_F"
CONSTR_FUNC_NAME = "pso_python.constr_F"

# problem dependent variables
LB = [[0.21, 0, 0.1]]        # Lower boundaries
UB = [[1, 1, 0.5]]           # Upper boundaries
OUT_VARS = 2                 # Number of output variables (y-values)
TARGETS = [0, 0]             # Target values for output
