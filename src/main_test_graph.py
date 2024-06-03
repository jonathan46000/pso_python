#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_python
#   './src/pso_python/main_test_graph.py'
#   Test function/example for using the 'swarm' class in particle_swarm.py.
#       This has been modified from the original to include message 
#       passing back to the parent class or testbench, rather than printing
#       error messages directly from the 'swarm' class. Format updates are 
#       for integration in the AntennaCAT GUI.
#       This version builds from 'pso_test_details.py' to include a 
#       matplotlib plot of particle location
#
#   Author(s): Lauren Linkous, Jonathan Lundquist,
#   Last update: June 3, 2024
##--------------------------------------------------------------------\


import numpy as np
import time
import matplotlib.pyplot as plt
from particle_swarm import swarm
import configs_F as func_configs


class psoTestDetails():
    def __init__(self):
        # Constant variables
        NO_OF_PARTICLES = 50         # Number of particles in swarm
        T_MOD = 0.65                 # Variable time-step extinction coefficient
        E_TOL = 10 ** -6             # Convergence Tolerance
        MAXIT = 5000                 # Maximum allowed iterations
        BOUNDARY = 1                 # int boundary 1 = random,      2 = reflecting
                                    #              3 = absorbing,   4 = invisible


        # Objective function dependent variables
        func_F = func_configs.OBJECTIVE_FUNC  # objective function
        constr_F = func_configs.CONSTR_FUNC   # constraint function

        LB = func_configs.LB              # Lower boundaries, [[0.21, 0, 0.1]]
        UB = func_configs.UB              # Upper boundaries, [[1, 1, 0.5]]   
        WEIGHTS = [[0.7, 1.5, 0.5]]       # Update vector weights
        VLIM = 0.5                        # Initial velocity limit
        OUT_VARS = func_configs.OUT_VARS  # Number of output variables (y-values)
        TARGETS = func_configs.TARGETS    # Target values for output

        # Swarm setting values
        parent = self                 # Optional parent class for swarm 
                                        # (Used for passing debug messages or
                                        # other information that will appear 
                                        # in GUI panels)

        detailedWarnings = False      # Optional boolean for detailed feedback


        # Swarm vars
        self.best_eval = 1            # Starting eval value

        parent = self                 # Optional parent class for swarm 
                                        # (Used for passing debug messages or
                                        # other information that will appear 
                                        # in GUI panels)

        self.suppress_output = True   # Suppress the console output of particle swarm

        detailedWarnings = False      # Optional boolean for detailed feedback
                                        # (Independent of suppress output. 
                                        #  Includes error messages and warnings)

        self.allow_update = True      # Allow objective call to update state 
                                        # (Can be set on each iteration to allow 
                                        # for when control flow can be returned 
                                        # to multiglods)


        self.mySwarm = swarm(NO_OF_PARTICLES, LB, UB,
                        WEIGHTS, VLIM, OUT_VARS, TARGETS,
                        T_MOD, E_TOL, MAXIT, BOUNDARY, func_F, constr_F, parent, detailedWarnings)  


        # Matplotlib setup
        self.targets = TARGETS
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.scatter = None


    def debug_message_printout(self, txt):
        if txt is None:
            return
        # sets the string as it gets it
        curTime = time.strftime("%H:%M:%S", time.localtime())
        msg = "[" + str(curTime) +"] " + str(txt)
        print(msg)


    def record_params(self):
        # this function is called from particle_swarm.py to trigger a write to a log file
        # running in the AntennaCAT GUI to record the parameter iteration that caused an error
        pass
         

    def update_plot(self, coords, targets, showTarget, clearAx=True, setLimts=False):
        # if self.scatter is None:
        if clearAx == True:
            self.ax.clear() #use this to git rid of the 'ant tunnel' trails
        if setLimts == True:
            self.ax.set_xlim(-.5, 3)
            self.ax.set_ylim(-.5, 3)
            self.ax.set_zlim(-.5, 3)
        
        if np.shape(coords)[0] == 2: #2-dim obj func
            self.ax.set_xlabel("$F_{1}(x,y)$")
            self.ax.set_ylabel("$F_{2}(x,y)$")
            self.scatter = self.ax.scatter(coords[0, :], coords[1, :])

        elif np.shape(coords)[0] == 3: #3-dim obj fun
            self.ax.set_xlabel("$F_{1}(x,y)$")
            self.ax.set_ylabel("$F_{2}(x,y)$")
            self.ax.set_zlabel("$F_{3}(x,y)$")
            self.scatter = self.ax.scatter(coords[0, :], coords[1, :], coords[2, :])

        if showTarget == True: # plot the target point
            if len(targets) == 1:
                self.scatter = self.ax.scatter(targets[0], 0)
            if len(targets) == 2:
                self.scatter = self.ax.scatter(targets[0], targets[1])
            elif len(targets) == 3:
                self.scatter = self.ax.scatter(targets[0], targets[1], targets[2])


        plt.pause(0.0001)  # Pause to update the plot




    def run_PSO(self):

        # instantiation of particle swarm optimizer 
        while not self.mySwarm.complete():

            # step through optimizer processing
            self.mySwarm.step(self.suppress_output)

            # call the objective function, control 
            # when it is allowed to update and return 
            # control to optimizer
            self.mySwarm.call_objective(self.allow_update)
            iter, eval = self.mySwarm.get_convergence_data()
            if (eval < self.best_eval) and (eval != 0):
                self.best_eval = eval
            if self.suppress_output:
                if iter%100 ==0: #print out every 100th iteration update
                    print("Iteration")
                    print(iter)
                    print("Best Eval")
                    print(self.best_eval)
            coords = self.mySwarm.M  #get x,y,z coordinate locations
            self.update_plot(coords, self.targets, showTarget=True) #update matplot

        print("Optimized Solution")
        print(self.mySwarm.get_optimized_soln())
        print("Optimized Outputs")
        print(self.mySwarm.get_optimized_outs())


if __name__ == "__main__":
    pso = psoTestDetails()
    pso.run_PSO()
