import matplotlib.pyplot as plt 
from simulation import Simulation 
import numpy as np 
import sys 
import networkx as nx 

# Parameters needed for simulation
simulation_time = 30
n = 5
intended_speed = (80 * 1000)/3600 
sim = Simulation(time = simulation_time, avStep = 100)
colors = ['red','blue','black','green','pink']

if sim:
    # Dictionary handling the coordinates of each edge
    pos = {
        "a":(60,10),
        "b":(60,190),
        "c":(190,190),
        "d":(190,10)
    }
    # Getting the start of the road from the graph 
    positions = list(pos.values())
    start = positions[0][1]

    # Variables and  parameters for animation 
    #fig, ax = plt.subplots()  
    points = []

    # Trying to make a graph lol 
    graph = nx.Graph() 
    graph.add_nodes_from(pos.keys())
    #Position of the node as node atrribute 
    for d, p in pos.items():
        graph.nodes[d]['pos'] = p 

    graph.add_edge("a","b")
    graph.add_edge("b","c")
    graph.add_edge("c","d")
    graph.add_edge("d","a")

    nx.draw(graph,pos)
    g = sim.rung_gipps_graph(n,intended_speed,start,pos,randomness=False,
            reac_time=2/3)
    #Animation
    #plt.figure(figsize=(10,4.8))
    for i in range(len(g.platoon[0].lrecords)):
        for p in points:
            p.remove()

        points = []

        for j in range(n):    
             
            #plt.xlim(g.platoon[0].lrecords[0][2],g.platoon[0].lrecords[-1][2]) # Max and min location 
            # This workaround make a zooom of the cars 
            plt.xlim(50,200) # Max and min location 
            plt.ylim(0,200) # Road 
            #points.append(plt.scatter(g.platoon[j].lrecords[i][2],start,marker='s',color=colors[j]))
            points.append(plt.scatter(g.platoon[j].position[i][0],g.platoon[j].position[i][1],marker='s',color=colors[j]))
            plt.xlabel("Vehicle location")
            plt.axis('off')
            #path = "images/test" + str(i) + ".png"
            #plt.savefig(path)
            plt.pause(0.01)
            
    plt.show()      
