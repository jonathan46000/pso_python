#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   './pso_basic/src/main_test_graph.py'
#   Test function/example for using the 'swarm' class in particle_swarm.py.
#       This has been modified from the original to include message 
#       passing back to the parent class or testbench, rather than printing
#       error messages directly from the 'swarm' class. Format updates are 
#       for integration in the AntennaCAT GUI.
#       This version builds from 'pso_test_details.py' to include a 
#       matplotlib plot of particle location
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: March 12, 2025
##--------------------------------------------------------------------\


import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from particle_swarm import swarm



# OBJECTIVE FUNCTION SELECTION
#import one_dim_x_test.configs_F as func_configs     # single objective, 1D input
#import himmelblau.configs_F as func_configs         # single objective, 2D input
import lundquist_3_var.configs_F as func_configs     # multi objective function



class TestGraph():
    def __init__(self):
        self.ctr = 0

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




        # Matplotlib setup
        self.targets = TARGETS
        self.fig = plt.figure(figsize=(10, 5))#(figsize=(14, 7))
        # position
        self.ax1 = self.fig.add_subplot(121, projection='3d')
        self.ax1.set_title("Particle Location, Iteration: " + str(self.ctr))
        self.ax1.set_xlabel('x_1')
        self.ax1.set_ylabel('x_2')
        self.ax1.set_zlabel('x_3')
        self.scatter1 = None
        # fitness
        self.ax2 = self.fig.add_subplot(122, projection='3d')
        self.ax2.set_title("Fitness Relation to Target")
        self.ax1.set_xlabel('x_1')
        self.ax1.set_ylabel('x_2')
        self.ax1.set_zlabel('x_3')
        self.scatter2 = None

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
         

    def update_plot(self, x_coords, y_coords, targets, showTarget=True, clearAx=True):
        
        # check if any points. first call might not have anythign set yet.
        if len(x_coords) < 1:
            return 


        if clearAx == True:
            self.ax1.clear() #use this to git rid of the 'ant tunnel' trails
            self.ax2.clear()

        # MOVEMENT PLOT
        if np.shape(x_coords)[1]==1: # 1 dim function
            x_plot_coords = np.array(x_coords[:,0])*0.0
            self.ax1.set_title("Search Locations, Iteration: " + str(self.ctr))
            self.ax1.set_xlabel("$x_1$")
            self.ax1.set_ylabel("filler coords")
            self.ax1.set_zlabel("filler coords")
            self.scatter = self.ax1.scatter(x_coords, x_plot_coords, edgecolors='b')   
        
        elif np.shape(x_coords)[1] == 2: #2-dim func
            self.ax1.set_title("Search Locations, Iteration: " + str(self.ctr))
            self.ax1.set_xlabel("$x_1$")
            self.ax1.set_ylabel("$x_2$")
            self.ax1.set_zlabel("filler coords")            
            self.scatter = self.ax1.scatter(x_coords[:,0], x_coords[:,1], edgecolors='b')

        elif np.shape(x_coords)[1] == 3: #3-dim func
            self.ax1.set_title("Search Locations, Iteration: " + str(self.ctr))
            self.ax1.set_xlabel("$x_1$")
            self.ax1.set_ylabel("$x_2$")
            self.ax1.set_zlabel("$x_3$")
            self.scatter = self.ax1.scatter(x_coords[:,0], x_coords[:,1], x_coords[:,2], edgecolors='b')


        # FITNESS PLOT
        if np.shape(y_coords)[1] == 1: #1-dim obj func
            y_plot_filler = np.array(y_coords[:,0])*0.0
            self.ax2.set_title("Global Best Fitness Relation to Target")
            self.ax2.set_xlabel("$F_{1}(x_1,x_2)$")
            self.ax2.set_ylabel("filler coords")
            self.ax2.set_zlabel("filler coords")
            self.scatter = self.ax2.scatter(y_coords, y_plot_filler,  marker='o', s=40, facecolor="none", edgecolors="k")

        elif np.shape(y_coords)[1] == 2: #2-dim obj func
            self.ax2.set_title("Global Best Fitness Relation to Target")
            self.ax2.set_xlabel("$F_{1}(x_1,x_2)$")
            self.ax2.set_ylabel("$F_{2}(x_1,x_2)$")
            self.ax2.set_zlabel("filler coords")
            self.scatter = self.ax2.scatter(y_coords[:,0], y_coords[:,1], marker='o', s=40, facecolor="none", edgecolors="k")

        elif np.shape(y_coords)[1] == 3: #3-dim obj fun
            self.ax2.set_title("Global Best Fitness Relation to Target")
            self.ax2.set_xlabel("$F_{1}(x_1,x_2)$")
            self.ax2.set_ylabel("$F_{2}(x_1,x_2)$")
            self.ax2.set_zlabel("$F_{3}(x_1,x_2)$")
            self.scatter = self.ax2.scatter(y_coords[:,0], y_coords[:,1], y_coords[:,2], marker='o', s=40, facecolor="none", edgecolors="k")


        if showTarget == True: # plot the target point
            if len(targets) == 1:
                self.scatter = self.ax2.scatter(targets[0], 0, marker='*', edgecolors='r')
            if len(targets) == 2:
                self.scatter = self.ax2.scatter(targets[0], targets[1], marker='*', edgecolors='r')
            elif len(targets) == 3:
                self.scatter = self.ax2.scatter(targets[0], targets[1], targets[2], marker='*', edgecolors='r')


        plt.pause(0.0001)  # Pause to update the plot
        if self.ctr == 0:
            time.sleep(2)

        self.ctr = self.ctr + 1

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
            m_coords = self.myOptimizer.M  #get x,y,z coordinate locations
            f_coords = self.myOptimizer.F_Gb # global best of set
            self.update_plot(m_coords, f_coords, self.targets, showTarget=True, clearAx=True) #update matplot

        print("Optimized Solution")
        print(self.myOptimizer.get_optimized_soln())
        print("Optimized Outputs")
        print(self.myOptimizer.get_optimized_outs())


        print("Optimization ended. Figure closing in 15 seconds.")
        time.sleep(15) #keep the window open for 15 seconds before ending program

if __name__ == "__main__":
    pso = TestGraph()
    pso.run()
