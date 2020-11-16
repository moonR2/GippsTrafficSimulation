import matplotlib.pyplot as plt
from simulation import Simulation
import numpy as np 
import sys 
import numpy as np 

simulation_time = 40
n = 5
intended_speed = (80 * 1000)/3600 
sim = Simulation(time = simulation_time, avStep = 100)
colors = ['red','blue','black','green','pink']

# Running two different simulations
if sim: 
    g = sim.run_gipps_simulation_y(n,intended_speed,randomness=True,reac_time=2/3,y_location=100)
    
    
    points = []
    
    #Animation
    plt.figure(figsize=(10,4.8))
    for i in range(len(g.platoon[0].lrecords)):
        for p in points:
            p.remove()

        points = []


        for j in range(n):    
            #plt.xlim(g.platoon[0].lrecords[0][2],g.platoon[0].lrecords[-1][2]) # Max and min location 
            plt.xlim(0,250) # Max and min location 
            plt.ylim(0,200) # Road 
            points.append(plt.scatter(g.platoon[j].lrecords[i][2],g.platoon[j].lrecords[i][4],marker='s',color=colors[j]))
            plt.xlabel("Vehicle location")
            #plt.axis('off')
            #path = "images/test" + str(i) + ".png"
            #plt.savefig(path)
            plt.pause(0.05)
            
    plt.show()      
    