import matplotlib.pyplot as plt
from simulation import Simulation
import sys 
import numpy as np 
import networkx as nx
""" 
This file plots trajectory, acceleration vs speed, speed vs simulation time
speed vs simulation times with bracking and vehicle location vs simulation time
wiht bracking vehicle. Also saves the data in a log.txt file. If you want an 
animation for the simulation run animation.py 
"""
# Simulation parameters 
simulation_time = 120  
n = 3
intended_speed = (80 * 1000)/3600 
sim = Simulation(time = simulation_time, avStep = 100)
# Colors of vehicles  
colors = ['red','blue','black','green','pink']
def plot_trajectory(platoon,x_max,y_max):
    vec = []
    for i in range(len(platoon)):
        for j in range(len(platoon[0].lrecords)):
            vec.append(platoon[i].lrecords[j][2])

        ylabelmap = str("Vehicle: %d" %(i+1))
        plt.ylabel("Vehicle Location $(m)$")
        plt.xlabel("Simulation Time $(sec)$")
        plt.legend("Vehicle n")
        plt.xlim(0,x_max)
        plt.ylim(0,y_max)
        plt.grid()
        plt.plot(platoon[0].ltime,vec,label=ylabelmap)
        L = plt.legend()
        L.get_texts()[i].set_text(ylabelmap)
        vec = []
    plt.savefig("images/LocationVsTime.png")

def plot_speed(platoon,x_max,y_max): 
    vec = []
    for i in range(len(platoon)):
        for j in range(len(platoon[0].lrecords)):
            vec.append(platoon[i].lrecords[j][1])

        ylabelmap = str("Vehicle: %d" %(i+1))
        plt.ylabel("Speed $(m/sec)$")
        plt.xlabel("Simulation Time $(sec)$")
        plt.legend("Vehicle n")
        plt.xlim(0,x_max)
        plt.ylim(0,y_max)
        plt.grid()
        plt.plot(platoon[0].ltime,vec,label=ylabelmap)
        L = plt.legend()
        L.get_texts()[i].set_text(ylabelmap)
        vec = []
    plt.savefig("images/SpeedVsTime.png")

def get_max_val(lrecords,i):
    return max([sublist[i] for sublist in lrecords])

def plot_acc_speed(vehicle,x_max,y_max): 
    acc = []
    spp = []
    for i in range(len(vehicle.lrecords)):
        acc.append(vehicle.lrecords[i][0])
        spp.append(vehicle.lrecords[i][1])

        plt.ylabel("Acceleration $(m/sec^2)$")
        plt.xlabel("Speed $(m/sec)$")
        plt.xlim(0,x_max)
        plt.ylim(0,y_max)
        plt.grid() 
        plt.plot(spp,acc)

    plt.savefig("images/AccVsSpeed.png")
    

def plot_acc(platoon,x_max, y_max): 
    acc = []
    for i in range(len(platoon)):
        for j in range(len(platoon[0].lrecords)):
            acc.append(platoon[i].lrecords[j][0])

        ylabelmap = str("Vehicle: %d" %(i+1))
        plt.ylabel("Acceleration $(m/sec^2)$")
        plt.xlabel("Simulation Time $(sec)$")
        plt.legend("Vehicle n")
        plt.xlim(0,x_max)
        plt.ylim(0,y_max)

        plt.grid()
        plt.plot(platoon[0].ltime,acc,label=ylabelmap)
        L = plt.legend()
        L.get_texts()[i].set_text(ylabelmap)
        acc = []
    plt.savefig("images/AccVsTime.png")
    
    
    

if sim:

    g = sim.run_gipps_simulation(n,intended_speed,randomness=False,reac_time=2/3,y_location=100)
    #g = sim.run_gipps_simulation_braking(n,intend_speed=intended_speed,sim_length_after_stop=10,
                                        #stop_veh_idx=3,randomness=False,react_time=2/3)
    if(len(sys.argv) > 1):
        # Debug mode prints data in console     
        if (sys.argv[1] == '-d' or sys.argv[1] == '-D'):
            print("Running in debug mode")
            for i in range(len(g.platoon[0].lrecords)):
                print("Simulation Time: ", g.platoon[0].ltime[i])
                for j in range(n):
                    print("V" + str(j) + ": ", g.platoon[j].lrecords[i])
        if(sys.argv[1] == '-c' or sys.argv[1] == '-C'):
            c = sim.run_gipps_congested(n,intended_speed,randomness=False,reac_time=2/3,y_location=100)
            print("Running Gipps Congested Model simulation")
            print("Simulation Time : [Acceleration, Speed, Location, Headway]") 


            print("Running simulation for: ", n, "cars.")
            print("Simulation data will be saved in log_congested.txt")
            f = open("log_congested.txt","w+")
            f.write("Gipps following-car congested model simulation \n")
            f.write("Simulation Time : [Acceleration, Speed, Location, Headway]\n")

            print("Running Gipps simulation")
            print("Simulation Time : [Acceleration, Speed, Location, Headway]") 
            
            for i in range(len(c.platoon[0].lrecords)):
                f.write("Simulation Time: %f \n" % c.platoon[0].ltime[i])
                for j in range(n):
                    handler = c.platoon[j].lrecords[i]
                    f.write("V%d: [%f,%f,%f,%f] \n" % (j, handler[0],handler[1],handler[2],handler[3]))
            print("Running Gipps simulation")
            print("Simulation Time : [Acceleration, Speed, Location, Headway]") 


    print("Running simulation for: ", n, "cars.")
    print("Simulation data will be saved in log.txt")
    f = open("log.txt","w+")
    f.write("Gipps following-car model simulation \n")
    f.write("Simulation Time : [Acceleration, Speed, Location, Headway]\n")

    print("Running Gipps simulation")
    print("Simulation Time : [Acceleration, Speed, Location, Headway]") 
    
    for i in range(len(g.platoon[0].lrecords)):
        f.write("Simulation Time: %f \n" % g.platoon[0].ltime[i])
        for j in range(n):
            handler = g.platoon[j].lrecords[i]
            f.write("V%d: [%f,%f,%f,%f] \n" % (j, handler[0],handler[1],handler[2],handler[3]))
        

    
    #Acc vs Time plot 
    x_max = g.platoon[0].ltime[-1]
    y_max = get_max_val(g.platoon[0].lrecords,0)
    plot_acc(g.platoon,x_max,y_max+0.02)
    plt.show()  
    
    # Acc vs Speed 
    x_max2 = get_max_val(g.platoon[0].lrecords,1)
    y_max2 = get_max_val(g.platoon[0].lrecords,0)
    plot_acc_speed(g.platoon[0],x_max2,y_max2+0.02)
    plt.show() 

    # Speed vs Time plot 
    x_max = g.platoon[0].ltime[-1]
    y_max = get_max_val(g.platoon[0].lrecords,1)
    plot_speed(g.platoon,x_max,y_max+0.02)
    plt.show()  

    # Location vs Time plot 
    x_max = g.platoon[0].ltime[-1]
    y_max = get_max_val(g.platoon[0].lrecords,2)
    plot_trajectory(g.platoon,x_max,y_max+0.02)
    plt.show()  


