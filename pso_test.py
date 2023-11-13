#! /usr/bin/python3
import numpy as np
from particle_swarm import swarm
from func_F import func_F

NO_OF_PARTICLES = 50         # Number of particles in swarm
LB = [[0, 0, 0]]             # Lower boundaries
UB = [[1, 1, 1]]             # Upper boundaries
WEIGHTS = [[0.7, 1.5, 0.5]]  # Update vector weights
VLIM = 0.3                   # Initial velocity limit
OUT_VARS = 2                 # Number of output variables (y-values)
TARGETS = [0, 0]             # Target values for output
T_MOD = 3                    # Variable time-step extinction coefficient
E_TOL = 10 ** -6             # Convergence Tolerance
MAXIT = 100000               # Maximum allowed iterations

suppress_output = False  # Suppress the console output of particle swarm

allow_update = True      # Allow objective call to update state 
                         # (Can be set on each iteration to allow 
                         # for when control flow can be returned 
                         # to multiglods)

mySwarm = swarm(NO_OF_PARTICLES, LB, UB,
                WEIGHTS, VLIM, OUT_VARS, TARGETS,
                T_MOD, E_TOL, MAXIT, func_F)  

# instantiation of particle swarm optimizer 
while not mySwarm.complete():

    # step through optimizer processing
    mySwarm.step(suppress_output)

    # call the objective function, control 
    # when it is allowed to update and return 
    # control to optimizer
    mySwarm.call_objective(allow_update)




