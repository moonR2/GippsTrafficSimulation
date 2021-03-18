import matplotlib.pyplot as plt
from simulation import Simulation
from objects.road import road, street
from statistics import mean 
import numpy as np
import sys
import networkx as nx

# Parameters needed for simulation
simulation_time = 60
n = 20
#intended_speed = (80 * 1000) / 3600  # 22,22
intended_speed = 20  # 22,22
sim = Simulation(time=simulation_time, avStep=100)
colors = ["red", "blue", "black", "green", "pink"]
streets = []
if sim:
    # Dictionary handling the coordinates of each edge
    pos = {
        "a": (10, 0),
        "b": (160, 0),
        "c": (310,0), 
        "d": (460,0),
        "e": (640,0),
        "a1": (10,300),
        "a2": (10,450),
        "a3": (10,600),
        "a4": (10,750),
        "b0": (160,150),
        "b1": (160,300),
        "b2": (160,450),
        "b3": (160,600),
        "b4": (160,750),
        "c0": (310,150),
        "c2": (310,450),
        "c3": (310,600),
        "c4": (310,750),
        "d0": (460,150),
        "d2": (460,450),
        "d3": (460,600),
        "d4": (460,750),
        "e0": (640,150),
        "e2": (640,450),
        "e3": (640,600),
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
        ("a","b"),
        ("b","c"),
        ("c","d"),
        ("d","e"),
        ("a","a1"),
        ("a1","a2"),
        ("a2","a3"),
        ("a3","a4"),
        ("b4","b3"),
        ("b3","b2"),
        ("b2","b1"),
        ("b1","b0"),
        ("b0","b"),
        ("c","c0"),
        ("c0","c2"),
        ("c2","c3"),
        ("c3","c4"),
        ("d4","d3"),
        ("d3","d2"),
        ("d2","d0"),
        ("d0","d"),
        ("e","e0"),
        ("e0","e2"),
        ("e2","e3"),
# ------------------------------------------------- Horizontal
        ("e0","d0"),
        ("d0","c0"),
        ("c0","b0"),
        ("b1","a1"),
        ("a2","b2"),
        ("b2","c2"),
        ("c2","d2"),
        ("d2","e2"),
        ("e3","d3"),
        ("d3","c3"),
        ("c3","b3"),
        ("b3","a3"),
        ("a4","b4"),
        ("b4","c4"),
        ("c4","d4"),
# ------------------------------------------------- Inclinado
        ("a","b1"),
        ("e3","d4")
    ]
    graph.add_edges_from(edges_list)

    # Testing road class 
    means = []
    n_vehicles = []
    st = street()
    for i in range(len(edges_list)):
        new_road = road(edges_list[i],pos,i)
        st.add_street(new_road)

    a_route = nx.shortest_path(graph, "a", "d")
    for i in range(200):
        speeds = []
        platoons = []
        total_pass = 0
        # run simulation 50 times
        for i in range(10):
            st = street()
            for j in range(len(edges_list)):
                new_road = road(edges_list[j],pos,j)
                st.add_street(new_road)
            #print("\nSimulation:",i)
            g = sim.run_xy(
                n, intended_speed, graph, pos, st, randomness=True, reac_time=2 / 3
            )
            del st
            platoons.append(g)

        for i in platoons:
            total_pass += i.vehPass
        
        for i in platoons:
            for j in range(n):
                if i.platoon[j].speed_pass_zero != None:
                    speeds.append(i.platoon[j].speed_pass_zero)
        print(len(speeds))
        print(mean(speeds)) 
        if len(speeds) > 1:
            means.append(np.round(np.mean(speeds),2))
        print("Total_pass",total_pass)
        # 50 / simulationTime = 0.83333
        vph = total_pass / 0.1666
        n_vehicles.append(vph)

    print(means) 
    print(n_vehicles)
    plt.xlabel("Flow $(vehicles/hour)$")
    plt.ylabel("Mean Speed $(m/s)$")
    plt.grid()
    plt.scatter(n_vehicles,means,linewidths=0.5)
    plt.show()
    path = "images/test" + "Density.png"
    plt.savefig(path)
    #print("Veh_pass",g.vehPass)
    #print("Delays:",g.delays)
    #print("N_platoons:",len(platoons))

    #g = sim.run_xy(
    #    n, intended_speed, graph, pos, st, randomness=True, reac_time=2 / 3
    #)
    ### Animation
    #nx.draw(graph, pos,with_labels=True, node_size = 200, node_color = "pink", width = 2.0, style = "dashed", label = "500m Road Link")
    #nx.draw_networkx_edges(graph, pos)
    #for i in range(len(g.platoon[0].lrecords)):
    #    for p in points:
    #        p.remove()

    #    points = []

    #    for j in range(n):

    #        # plt.xlim(g.platoon[0].lrecords[0][2],g.platoon[0].lrecords[-1][2]) # Max and min location
    #        # This workaround make a zooom of the cars
    #        length = g.platoon[j].lrecords[i][4]
    #        plt.xlim(-30,670) # Max and min location
    #        plt.ylim(-30,780) # Road
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
    #        #plt.savefig(path)
    #        plt.pause(0.01)
    #plt.show()
