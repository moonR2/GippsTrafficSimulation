import matplotlib.pyplot as plt
from simulation import Simulation
from objects.road import road, street
import numpy as np
import sys
import networkx as nx

# Parameters needed for simulation
simulation_time = 45
n = 3
intended_speed = (80 * 1000) / 3600  # 22,22
sim = Simulation(time=simulation_time, avStep=100)
colors = ["red", "blue", "black", "green", "pink"]
streets = []

if sim:
    # Dictionary handling the coordinates of each edge
    pos = {
        "a": (50, 0),
        "b": (50, 130),
        "c": (180, 130),
        "d": (180, 0),
        "e": (310, 0),
        "f": (310, 130),
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
        ("a", "c"),
        ("b","c"),
        #("c","d"),
        ("e","c"),
        ("d","a"),
        ("e","d"),
        ("f","e"),
        ("c","f")
    ]
    graph.add_edges_from(edges_list)

    # Testing road class 
    st = street()
    for i in range(len(edges_list)):
        new_road = road(edges_list[i],pos,i)
        st.add_street(new_road)

    for i in range(len(edges_list)):
        print("ID:",st.streets[i].ith)
        print("Nodes: ",st.streets[i].nodes)
        print("Start: ",st.streets[i].start)
        print("End: ",st.streets[i].end)
        print("END---")

    a_route = nx.shortest_path(graph, "a", "d")
    nx.draw(graph, pos, with_labels=True)
    nx.draw_networkx_edges(graph, pos)
    g = sim.run_xy(
        n, intended_speed, graph, pos, st, randomness=False, reac_time=2 / 3
    )
    # Animation
    for i in range(len(g.platoon[0].lrecords)):
        for p in points:
            p.remove()

        points = []

        for j in range(n):

            # plt.xlim(g.platoon[0].lrecords[0][2],g.platoon[0].lrecords[-1][2]) # Max and min location
            # This workaround make a zooom of the cars
            # plt.xlim(50,200) # Max and min location
            # plt.ylim(0,200) # Road
            # points.append(plt.scatter(g.platoon[j].lrecords[i][2],start,marker='s',color=colors[j]))
            points.append(
                plt.scatter(
                    g.platoon[j].position[i][0],
                    g.platoon[j].position[i][1],
                    marker="s",
                    color=colors[j],
                )
            )
            plt.xlabel("Vehicle location")
            plt.axis("off")
            # path = "images/test" + str(i) + ".png"
            # plt.savefig(path)
            plt.pause(0.01)
    plt.show()
