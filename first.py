import matplotlib.pyplot as plt
from simulation import Simulation
from objects.road import road, street
import numpy as np
import sys
import networkx as nx

# Parameters needed for simulation
simulation_time = 60
n = 10
intended_speed = (80 * 1000) / 3600  # 22,22
sim = Simulation(time=simulation_time, avStep=100)
colors = ["red", "blue", "black", "green", "pink"]
streets = []

def plot_trajectory(platoon,x_max,y_max):
    vec = []
    for i in range(len(platoon)):
        for j in range(len(platoon[0].lrecords)):
            vec.append(platoon[i].position[j][0])

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
    plt.savefig("images/LocationVsTimeNRNG.png")

def plot_speed(platoon,x_max,y_max): 
    vec = []
    for i in range(len(platoon)):
        for j in range(len(platoon[0].lrecords)):
            vec.append(platoon[i].lrecords[j][1])
            print(platoon[i].lrecords[j][1])

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
    plt.savefig("images/SpeedVsTimeNRNG.png")

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

    plt.savefig("images/AccVsSpeedNRNG.png")
    

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
    plt.savefig("images/AccVsTimeNRNG.png")

if sim:
    # Dictionary handling the coordinates of each edge
    pos = {
        "a": (10, 0),
        "b": (510, 0)
    }
    # Getting the start of the road from the graph
    positions = list(pos.values())
    start = positions[0][1]

    # Variables and  parameters for animation
    # fig, ax = plt.subplots()
    points = []

    # Trying to make a graph lol
    graph = nx.DiGraph()
    graph.add_nodes_from(pos.keys())
    # Position of the node as node atrribute
    for d, p in pos.items():
        graph.nodes[d]["pos"] = p

    edges_list = [
        ("a","b")
    ]
    graph.add_edges_from(edges_list)

    # Testing road class 
    st = street()
    for i in range(len(edges_list)):
        new_road = road(edges_list[i],pos,i)
        st.add_street(new_road)

    a_route = nx.shortest_path(graph, "a", "b")
    #nx.draw(graph, pos,with_labels=True, node_size = 200, node_color = "red", width = 2.0, style = "dashed", label = "500m Road Link")
    #nx.draw_networkx_edges(graph, pos)
    g = sim.run_xy(
        n, intended_speed, graph, pos, st, randomness=True, reac_time=2 / 3
    )
    # Animation
    #for i in range(len(g.platoon[0].lrecords)):
    #    for p in points:
    #        p.remove()

    #    points = []

    #    for j in range(n):

    #        # plt.xlim(g.platoon[0].lrecords[0][2],g.platoon[0].lrecords[-1][2]) # Max and min location
    #        # This workaround make a zooom of the cars
    #        length = g.platoon[j].lrecords[i][4]
    #        plt.xlim(-90,600) # Max and min location
    #        plt.ylim(-200,200) # Road
    #        # points.append(plt.scatter(g.platoon[j].lrecords[i][2],start,marker='s',color=colors[j]))
    #        points.append(
    #            plt.scatter(
    #                g.platoon[j].position[i][0],
    #                g.platoon[j].position[i][1],
    #                marker="s",
    #                color="blue",
    #                s=(length * 5)
    #            )
    #        )
    #        plt.xlabel("Vehicle location")
    #        plt.axis("off")
    #        path = "images/test" + str(i) + ".png"
    #        plt.savefig(path)
    #        plt.pause(0.01)
    #plt.show()

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

# Acc vs Speed 
#    x_max2 = get_max_val(g.platoon[0].lrecords,1)
#    y_max2 = get_max_val(g.platoon[0].lrecords,0)
#    plot_acc_speed(g.platoon[0],x_max2,y_max2+0.02)
#    plt.show() 

# Speed vs Time plot 
    x_max = g.platoon[0].ltime[-1]
    y_max = get_max_val(g.platoon[0].lrecords,1)
    plot_speed(g.platoon,x_max,y_max+0.02)
    plt.grid()
    plt.show()  

    # Location vs Time plot 
    x_max = g.platoon[0].ltime[-1]
    y_max = 1000
    plot_trajectory(g.platoon,x_max,y_max+0.02)
    plt.grid()
    plt.show() 