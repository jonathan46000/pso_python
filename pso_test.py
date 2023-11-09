import numpy as np
from particle_swarm import swarm
from func_F import func_F


# arguments should take form: 
    # swarm(int, [[float, float, ...]], 
    # [[float, float, ...]], [[float, ...]], 
    # float, int, [float, ...], float, 
    # float, int, func)

mySwarm = swarm(50, [[0, 0, 0]], [[1, 1, 1]],
                [[0.7, 1.5, 0.5]], 0.3, 2, [0, 0],
                3, 1e-6, 100000, func_F)  


while not mySwarm.complete():
    print(mySwarm.iter)
    print(np.linalg.norm(mySwarm.F_Gb))
    mySwarm.NON_ANCAT_GLOBAL_UPDATE()

print("iter | M | V | Gb | F_Gb")
print(mySwarm.iter)
print(mySwarm.M)
print(mySwarm.V)
print(mySwarm.Gb)
print(mySwarm.F_Gb)
