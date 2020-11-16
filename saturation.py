import matplotlib.pyplot as plt
from simulation import Simulation
import numpy as np 
import sys 
import numpy as np 

simulation_time = 200
n = 100
intended_speed = (80 * 1000)/3600 
sim = Simulation(time = simulation_time, avStep = 100)

def saturation_flow(g):
    start = 0
    start_car = g.platoon[start].time_pass_zero
    #print(start_car)
    last_car = g.platoon[g.vehPass-1].time_pass_zero
    #print(last_car)
    t_dif = (last_car - start_car)/1000
    return (g.vehPass - start)/t_dif * 3600

def get_average_spedd(g):
    sum = 0 
    for i in range(n):
        sum += g.platoon[i].speed_pass_zero
    return sum/n

if sim: 
    saturation_flow_y = []
    speed_flow_x = []
    for i in range(100):
        g2 = sim.run_gipps_simulation(n,intended_speed,randomness=True,reac_time=2/3)
        saturation_flow_y.append(saturation_flow(g2))
        speed_flow_x.append(get_average_spedd(g2))

        



    #print(saturation_flow_y)
    #print(len(saturation_flow_y), len(g.platoon[0].lrecords))
    #print(len(speed_flow_x), speed_flow_x)

    plt.scatter(saturation_flow_y,speed_flow_x,marker='.')
    plt.savefig("images/saturation.png")
    plt.show() 