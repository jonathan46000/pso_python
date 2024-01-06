# pso_python
Simple adaptive timestep particle swarm optimizer written in Python

## Times-step adaptation 
This particle swarm optimizers using the mean absolute deviation of particle position
as an adjustment to the time step, to prevent the particle overshoot problem.  This 
particle distribution is initialized to one when the swarm starts, so that the impact
is boundary independent. 

## Constraint handling
Users must create thier own constraint function for thier problems, if there are  constraints
beyond the problem bounds.  This is then passed into the constructor. If the default constraint
function is used, it always returns true (which means there are no constraints).

## Boundry types
This PSO optimizers has 4 different types of bounds, Random (Particles that leave the area respawn),
Reflection (Particles that hit the bounds reflect), Absorb (Particles that hit the bounds lose velocity
in that direction), Invisible (Out of bound particles are no longer evaluated).

Some updates have not incorporated appropariate handling for all boundry conditions.  This bug is known
and is being worked on.  The most consistent boundary type at the moment is Random.  If constraints are
violated, but bounds are not, currently random bound rules are used to deal with this problem. 

## Multi-Object Optimization
The no preference method of multi-objective optimization, but a Pareto Front is not calculated.
Instead the best choice (smallest norm of output vectors) is listed as the output.

## Objective function handling
The optimizer minimizes the absolute value of the difference from the targets outputs and the
evaluated outputs.  Future versions may include options for function minimization absent target
values. 

## Example implimentation
PSO_TEST.py provides a sample use case of the optimizer. 
