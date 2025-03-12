#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   './pso_basic/src/main_test_details.py'
#   Test function/example for using the 'swarm' class in particle_swarm.py.
#       This has been modified from the original to include message 
#       passing back to the parent class or testbench, rather than printing
#       error messages directly from the 'swarm' class. Format updates are 
#       for integration in the AntennaCAT GUI.
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: March 12, 2025
##--------------------------------------------------------------------\


import pandas as pd
import time
from particle_swarm import swarm


# OBJECTIVE FUNCTION SELECTION
#import one_dim_x_test.configs_F as func_configs     # single objective, 1D input
#import himmelblau.configs_F as func_configs         # single objective, 2D input
import lundquist_3_var.configs_F as func_configs     # multi objective function



class TestDetails():
    def __init__(self):
        # Constant variables
        NO_OF_PARTICLES = 11         # Number of particles in swarm
        TOL = 10 ** -18              # Convergence Tolerance
        MAXIT = 10000                # Maximum allowed iterations
        BOUNDARY = 1                 # int boundary 1 = random,      2 = reflecting
                                    #              3 = absorbing,   4 = invisible

        # Objective function dependent variables
        func_F = func_configs.OBJECTIVE_FUNC  # objective function
        constr_F = func_configs.CONSTR_FUNC   # constraint function

        LB = func_configs.LB              # Lower boundaries, [[0.21, 0, 0.1]]
        UB = func_configs.UB              # Upper boundaries, [[1, 1, 0.5]]   
        OUT_VARS = func_configs.OUT_VARS  # Number of output variables (y-values)
        TARGETS = func_configs.TARGETS    # Target values for output

        # optimizer constants
        WEIGHTS = [[0.5, 0.7, 0.78]]       # Update vector weights
        VLIM = 1                           # Initial velocity limit


        self.best_eval = 1
        parent = self                 # for passing debug back to the parent class
        self.suppress_output = True   # Suppress the console output of particle swarm
        self.allow_update = True      # Allow objective call to update state 


        # Constant variables in a list format
        opt_params = {'NO_OF_PARTICLES': [NO_OF_PARTICLES], # Number of particles in swarm
                    'BOUNDARY': [BOUNDARY],                 # int boundary 1 = random,      2 = reflecting
                                                            #   3 = absorbing,   4 = invisible
                    'WEIGHTS': [WEIGHTS],                   # Update vector weights
                    'VLIM':  [VLIM] }                       # Initial velocity limit

        # dataframe conversion
        opt_df = pd.DataFrame(opt_params)

        # optimizer initialization
        self.myOptimizer = swarm(LB, UB, TARGETS, TOL, MAXIT,
                                func_F, constr_F,
                                opt_df,
                                parent=parent)  


    def debug_message_printout(self, txt):
        if txt is None:
            return
        # sets the string as it gets it
        curTime = time.strftime("%H:%M:%S", time.localtime())
        msg = "[" + str(curTime) +"] " + str(txt)
        print(msg)


    def run(self):

        # instantiation of particle swarm optimizer 
        while not self.myOptimizer.complete():

            # step through optimizer processing
            self.myOptimizer.step(self.suppress_output)

            # call the objective function, control 
            # when it is allowed to update and return 
            # control to optimizer
            self.myOptimizer.call_objective(self.allow_update)
            iter, eval = self.myOptimizer.get_convergence_data()
            if (eval < self.best_eval) and (eval != 0):
                self.best_eval = eval
            if self.suppress_output:
                if iter%100 ==0: #print out every 100th iteration update
                    print("Iteration")
                    print(iter)
                    print("Best Eval")
                    print(self.best_eval)

        print("Optimized Solution")
        print(self.myOptimizer.get_optimized_soln())
        print("Optimized Outputs")
        print(self.myOptimizer.get_optimized_outs())



if __name__ == "__main__":
    pso = TestDetails()
    pso.run()
