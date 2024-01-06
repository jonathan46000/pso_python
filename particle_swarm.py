#! /usr/bin/python3
import numpy as np
from numpy.random import Generator, MT19937
import os
import sys


class swarm:

    # arguments should take form: 
    # swarm(int, [[float, float, ...]], 
    # [[float, float, ...]], [[float, ...]], 
    # float, int, [[float, ...]], float, 
    # float, int, int, func) 
    # int boundary 1 = random,      2 = reflecting
    #              3 = absorbing,   4 = invisible
    def __init__(self, NO_OF_PARTICLES, lbound, ubound,
                 weights, vlimit, output_size, targets,
                 T_MOD, E_TOL, maxit, boundary, obj_func,
                 constr_func):  

        heightl = np.shape(lbound)[0]
        widthl = np.shape(lbound)[1]
        heightu = np.shape(ubound)[0]
        widthu = np.shape(ubound)[1]

        lbound = np.array(lbound[0])
        ubound = np.array(ubound[0])

        self.rng = Generator(MT19937())

        if ((heightl > 1) and (widthl > 1)) \
           or ((heightu > 1) and (widthu > 1)) \
           or (heightu != heightl) \
           or (widthl != widthu):
            
            print("Error lbound and ubound must be 1xN-dimensional \
                  arrays  with the same length")

        else:
        
            if heightl == 1:
                lbound = np.vstack(lbound)
        
            if heightu == 1:
                ubound = np.vstack(ubound)

            self.lbound = lbound
            self.ubound = ubound
            variation = ubound-lbound

            self.M = np.vstack(np.multiply( self.rng.random((np.max([heightl, 
                                                                     widthl]),1)), 
                                                                     variation) + 
                                                                     lbound)      
            self.V = np.vstack(np.multiply( self.rng.random((np.max([heightl, 
                                                                     widthl]),1)), 
                                                                     vlimit))

            for i in range(2,NO_OF_PARTICLES+1):
                
                self.M = \
                    np.hstack([self.M, 
                               np.vstack(np.multiply( self.rng.random((np.max([heightl, 
                                                                               widthl]),
                                                                               1)), 
                                                                               variation) 
                                                                               + lbound)])
                self.V = \
                    np.hstack([self.V, 
                               np.vstack(np.multiply( self.rng.random((np.max([heightl, 
                                                                               widthl]),
                                                                               1)), 
                                                                               vlimit))])
        
            self.Active = np.ones((NO_OF_PARTICLES))
            self.Gb = sys.maxsize*np.ones((np.max([heightl, widthl]),1))
            self.F_Gb = sys.maxsize*np.ones((output_size,1))
            self.Pb = sys.maxsize*np.ones(np.shape(self.M))
            self.F_Pb = sys.maxsize*np.ones((output_size,NO_OF_PARTICLES))
            self.weights = np.vstack(np.array(weights))
            self.targets = np.vstack(np.array(targets))
            self.T_MOD = T_MOD
            self.maxit = maxit
            self.E_TOL = E_TOL
            self.obj_func = obj_func
            self.constr_func = constr_func
            self.iter = 0
            self.current_particle = 0
            self.number_of_particles = NO_OF_PARTICLES
            self.allow_update = 0
            self.boundary = boundary
            self.Flist = []
            self.Fvals = []
            self.vlimit = vlimit
            self.Mlast = 1*self.ubound
            self.InitDeviation = self.absolute_mean_deviation_of_particles() 
            self.delta_t = self.absolute_mean_deviation_of_particles()/(T_MOD*self.InitDeviation)
            

    def call_objective(self, parent, allow_update):
        if self.Active[self.current_particle]:
            self.Fvals = self.obj_func(parent, np.vstack(self.M[:,self.current_particle]))
            if allow_update:
                self.Flist = abs(self.targets - self.Fvals)
                self.iter = self.iter + 1
                self.allow_update = 1
            else:
                self.allow_update = 0  
    
    def update_velocity(self,particle):
        for i in range(0,np.shape(self.V)[0]):
            
            self.V[i,particle] = \
                self.weights[0][0]* self.rng.random()*self.V[i,particle] \
                    + self.weights[0][1]* self.rng.random() \
                        * (self.Pb[i,particle]-self.M[i,particle]) \
                            + self.weights[0][2]* self.rng.random() \
                                * (self.Gb[i]-self.M[i,particle])
            
    def check_bounds(self, particle):
        update = 0
        for i in range(0,(np.shape(self.M)[0])):
            if (self.lbound[i] > self.M[i,particle]) \
               or (self.ubound[i] < self.M[i,particle]):
                update = i+1
        return update

    def random_bound(self, particle):

        update = self.check_bounds(particle) or not self.constr_func(self.M[:,particle])

        if update > 0:
            while not self.constr_func(self.M[:,particle]):
                variation = self.ubound-self.lbound
                self.M[:,particle] = \
                    np.squeeze( self.rng.random() * 
                                np.multiply(np.ones((np.shape(self.M)[0],1)),
                                            variation) + self.lbound)
            
    def reflecting_bound(self, particle):
        
        update = self.check_bounds(particle)
        constr = self.constr_func(self.M[:,particle])
        if (update > 0) and constr:
            self.M[:,particle] = 1*self.Mlast
            NewV = np.multiply(-1,self.V[update-1,particle])
            self.V[update-1,particle] = NewV
        if not constr:
            self.random_bound(particle)

    def absorbing_bound(self, particle):
        
        update = self.check_bounds(particle)
        constr = self.constr_func(self.M[:,particle])
        if (update > 0) and constr:
            self.M[:,particle] = 1*self.Mlast
            self.V[update-1,particle] = 0
        if not constr:
            self.random_bound(particle)

    def invisible_bound(self, particle):
        
        update = self.check_bounds(particle) or not self.constr_func(self.M[:,particle])

        if update > 0:
            self.Active[particle] = 0            

    def handle_bounds(self, particle):
        if self.boundary == 1:
            self.random_bound(particle)
        elif self.boundary == 2:
            self.reflecting_bound(particle)
        elif self.boundary == 3:
            self.absorbing_bound(particle)
        elif self.boundary == 4:
            self.invisible_bound(particle)
        else:
            print("Error: No boundary is set!")

    def check_global_local(self, Flist, particle):

        if np.linalg.norm(Flist) < np.linalg.norm(self.F_Gb):
            self.F_Gb = Flist
            self.Gb = np.vstack(np.array(self.M[:,particle]))
        
        if np.linalg.norm(Flist) < np.linalg.norm(self.F_Pb[:,particle]):
            self.F_Pb[:,particle] = np.squeeze(Flist)
            self.Pb[:,particle] = self.M[:,particle]
    
    def update_point(self,particle):
        self.Mlast = 1*self.M[:,particle]
        self.M[:,particle] = self.M[:,particle] + self.delta_t*self.V[:,particle]

    def update_delta_t(self):
        self.delta_t = self.absolute_mean_deviation_of_particles()/(self.T_MOD*self.InitDeviation)

    def converged(self):
        convergence = np.linalg.norm(self.F_Gb) < self.E_TOL
        return convergence
    
    def maxed(self):
        max_iter = self.iter > self.maxit
        return max_iter
    
    def complete(self):
        done = self.converged() or self.maxed()
        return done
    
    def step(self, suppress_output):
        if not suppress_output:
            print("-----------------------------")
            print("STEP")
            print("-----------------------------")
            print("Current Particle:")
            print(self.current_particle)
            print("Current Particle Velocity")
            print(self.V[:,self.current_particle])
            print("Current Particle Location")
            print(self.M[:,self.current_particle])
            print("Delta T")
            print(self.delta_t)
            print("Absolute mean deviation")
            print(self.absolute_mean_deviation_of_particles())
            print("-----------------------------")
        if self.allow_update:
            if self.Active[self.current_particle]:
                self.check_global_local(self.Flist,self.current_particle)
                self.update_velocity(self.current_particle)
                self.update_point(self.current_particle)
                self.handle_bounds(self.current_particle)
            self.current_particle = self.current_particle + 1
            if self.current_particle == self.number_of_particles:
                self.current_particle = 0
                self.update_delta_t()
            if self.complete() and not suppress_output:
                print("Points:")
                print(self.Gb)
                print("Iterations:")
                print(self.iter)
                print("Flist:")
                print(self.F_Gb)
                print("Norm Flist:")
                print(np.linalg.norm(self.F_Gb))

    def export_swarm(self):
        swarm_export = {'lbound': self.lbound,
                        'ubound': self.ubound,
                        'M': self.M,
                        'V': self.V,
                        'Gb': self.Gb,
                        'F_Gb': self.F_Gb,
                        'Pb': self.Pb,
                        'F_Pb': self.F_Pb,
                        'weights': self.weights,
                        'targets': self.targets,
                        'T_MOD': self.T_MOD,
                        'maxit': self.maxit,
                        'E_TOL': self.E_TOL,
                        'iter': self.iter,
                        'delta_t': self.delta_t,
                        'current_particle': self.current_particle,
                        'number_of_particles': self.number_of_particles,
                        'allow_update': self.allow_update,
                        'Flist': self.Flist,
                        'Fvals': self.Fvals,
                        'Active': self.Active,
                        'Boundary': self.boundary,
                        'Mlast': self.Mlast}
        
        return swarm_export

    def import_swarm(self, swarm_export, obj_func):
        self.lbound = swarm_export['lbound'] 
        self.ubound = swarm_export['ubound'] 
        self.M = swarm_export['M'] 
        self.V = swarm_export['V'] 
        self.Gb = swarm_export['Gb'] 
        self.F_Gb = swarm_export['F_Gb'] 
        self.Pb = swarm_export['Pb'] 
        self.F_Pb = swarm_export['F_Pb'] 
        self.weights = swarm_export['weights'] 
        self.targets = swarm_export['targets'] 
        self.T_MOD = swarm_export['T_MOD'] 
        self.maxit = swarm_export['maxit'] 
        self.E_TOL = swarm_export['E_TOL'] 
        self.iter = swarm_export['iter'] 
        self.delta_t = swarm_export['delta_t'] 
        self.current_particle = swarm_export['current_particle'] 
        self.number_of_particles = swarm_export['number_of_particles'] 
        self.allow_update = swarm_export['allow_update'] 
        self.Flist = swarm_export['Flist'] 
        self.Fvals = swarm_export['Fvals']
        self.Active = swarm_export['Active']
        self.boundary = swarm_export['Boundary']
        self.Mlast = swarm_export['Mlast']
        self.obj_func = obj_func 

    def get_obj_inputs(self):
        return np.vstack(self.M[:,self.current_particle])
    
    def get_convergence_data(self):
        best_eval = np.linalg.norm(self.F_Gb)
        iteration = 1*self.iter
        return iteration, best_eval
        
    def get_optimized_soln(self):
        return self.Gb 
    
    def get_optimized_outs(self):
        return self.F_Gb
    
    def absolute_mean_deviation_of_particles(self):
        mean_data = np.vstack(np.mean(self.M,axis=1))
        abs_data = np.zeros(np.shape(self.M))
        for i in range(0,self.number_of_particles):
            abs_data[:,i] = np.squeeze(np.abs(np.vstack(self.M[:,i])-mean_data))
        abs_mean_dev = np.linalg.norm(np.mean(abs_data,axis=1))
        return abs_mean_dev
