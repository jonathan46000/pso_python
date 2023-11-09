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
    # float, int, func)
    def __init__(self, NO_OF_PARTICLES, lbound, ubound,
                 weights, vlimit, output_size, targets,
                 T_MOD, E_TOL, maxit, obj_func):  

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
            self.iter = 0
            self.delta_t = np.linalg.norm(self.M)/T_MOD
            

    def  f_eval(self,particle):
        
        Fvals = self.obj_func(np.vstack(self.M[:,particle]))
        Flist = abs(self.targets - Fvals)
        self.iter = self.iter + 1

        return Flist, Fvals   
    
    def update_velocity(self,particle):

        for i in range(0,np.shape(self.V)[0]):
            self.V[i,particle] = \
                self.weights[0][0]* self.rng.random()*self.V[i,particle] \
                    + self.weights[0][1]* self.rng.random() \
                        * (self.Pb[i,particle]-self.M[i,particle]) \
                            + self.weights[0][2]* self.rng.random() \
                                * (self.Gb[i]-self.M[i,particle])
        
        
    def cull_and_spawn(self,particle):

        update = 0
        for i in range(0,(np.shape(self.M)[0])):
            if (self.lbound[i] > self.M[i,particle]) \
               or (self.ubound[i] < self.M[i,particle]):
                update = 1

        if update:
            variation = self.ubound-self.lbound
            self.M[:,particle] = \
                np.squeeze( self.rng.random() * 
                           np.multiply(np.ones((np.shape(self.M)[0],1)),
                                       variation) + self.lbound)

    def check_global_local(self,Flist,particle):

        if np.linalg.norm(Flist) < np.linalg.norm(self.F_Gb):
            self.F_Gb = Flist
            self.Gb = np.vstack(np.array(self.M[:,particle]))
        
        if np.linalg.norm(Flist) < np.linalg.norm(self.F_Pb[:,particle]):
            self.F_Pb[:,particle] = np.squeeze(Flist)
            self.Pb[:,particle] = self.M[:,particle]
    
    def update_point(self,particle):
        self.M[:,particle] = self.M[:,particle] + self.delta_t*self.V[:,particle]

    def update_delta_t(self):
        self.delta_t = np.linalg.norm(self.M)/self.T_MOD

    def converged(self):
        convergence = np.linalg.norm(self.F_Gb) < self.E_TOL
        return convergence
    
    def maxed(self):
        max_iter = self.iter > self.maxit
        return max_iter
    
    def complete(self):
        done = self.converged() or self.maxed()
        return done
    
    def post_objective_point_update(self,Flist,particle):
            self.check_global_local(Flist,particle)
            self.update_velocity(particle)
            self.update_point(particle)
            self.cull_and_spawn(particle)

    def NON_ANCAT_GLOBAL_UPDATE(self):
        for i in range(0,np.shape(self.M)[1]):
            Flist, Fvals = self.f_eval(i)
            self.post_objective_point_update(Flist,i)
        self.update_delta_t()

        

        